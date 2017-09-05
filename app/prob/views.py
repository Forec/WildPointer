# -*- coding: utf-8 -*-
# @Time    : 2017/9/5 16:42
# @Author  : Forec
# @File    : prob/views.py
# @Project : WildPointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn


from flask import render_template, redirect, url_for, abort, flash, request, current_app
from flask_login import login_required, current_user
from sqlalchemy import or_

from . import prob
from .forms import SubmitCodeForm, EditTaskForm, SearchForm, ApplyForm
from .. import db
from ..models import Task, Permission, Code, Language, Advice
from ..decorators import admin_required, permission_required

@prob.route('/all_probs')
def all_probs():
    page = request.args.get('page', 1, type=int)
    pagination = Task.query.order_by(Task.timestamp.desc()).paginate(
        page, per_page=current_app.config['WP_TASKS_PER_PAGE'],
        error_out=False
    )
    tasks = pagination.items
    return render_template('prob/tasks.html', tasks = tasks,
                           pagination = pagination)

@prob.route('/task/<int:id>', methods=['GET','POST'])
def task(id):
    task = Task.query.get_or_404(id)
    form = SubmitCodeForm()
    page = request.args.get('page', 1, type=int)
    pagination = task.advices.order_by(Advice.timestamp.desc()).paginate(
        page, per_page=current_app.config['WP_ADVICES_PER_PAGE'],
        error_out=False
    )
    advices = pagination.items
    if form.validate_on_submit():
        code = Code(body = '```'+form.code.data+'```',
                    author =current_user._get_current_object(),
                    task = task,
                    language=Language.query.filter_by(id=form.language.data).first())
        db.session.add(code)
        db.session.commit()
        flash('您的代码已提交')
        return redirect(url_for('prob.task', id=id))
    return render_template('prob/task.html', tasks = [task], advices = advices,
                           pagination = pagination,form=form, id=id)

@prob.route('/edit_task/<int:id>', methods=['GET','POST'])
@login_required
def edit_task(id):
    task = Task.query.get_or_404(id)
    if current_user != task.publisher and \
        not current_user.can(Permission.ADMINISTER):
        abort(403)
    form = EditTaskForm()
    if form.validate_on_submit():
        task.title = form.title.data
        task.body = form.body.data
        db.session.add(task)
        db.session.commit()
        flash('任务已更新')
        return redirect(url_for('prob.task', id=task.id))
    form.body.data = task.body
    form.title.data = task.title
    return render_template('prob/edit_task.html', form = form)

@prob.route('/delete_task/<int:id>',methods=['GET','POST'])
@login_required
def delete_task(id):
    task= Task.query.get_or_404(id)
    if current_user != task.publisher and not current_user.can(Permission.ADMINISTER):
        abort(403)
    flash('小心！删除操作不能撤回！')
    form = EditTaskForm()
    if form.validate_on_submit():
        task.title = form.title.data
        task.body = form.body.data
        db.session.add(task)
        flash('任务已被更新')
        return redirect(url_for('prob.task',id = task.id))
    form.body.data=task.body
    form.title.data = task.title
    return render_template('prob/confirm_delete_task.html',task = task,form=form,
                           token=current_user.generate_delete_token(postid=id, expiration=3600))

@prob.route('/delete-task-confirm/<token>')
@login_required
def delete_task_confirm(token):
    if current_user.delete_task(token):
        flash('任务已被删除')
        return redirect(url_for('prob.all_probs'))
    else:
        abort(403)

@prob.route('/moderate_tasks', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.MODERATE_TASKS)
def moderate_tasks():
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for('prob.moderate_tasks', key=form.key.data))
    page = request.args.get('page', 1, type=int)
    key = request.args.get('key', '', type=str)
    if key == '':
        task = Task.query
    else:
        task = Task.query.filter(or_(Task.title.like('%'+key+'%'),Task.body.like('%'+key+'%')))
    pagination = task.order_by(Task.timestamp.desc()).paginate(
        page, per_page=current_app.config['WP_TASKS_PER_PAGE'],
        error_out=False)
    tasks = pagination.items
    form.key.data = key
    return render_template('prob/moderate_tasks.html', tasks=tasks,
                           pagination=pagination, page=page, form=form)

@prob.route('/moderate_tasks/set_nobug/<int:id>')
@login_required
@permission_required(Permission.MODERATE_TASKS)
def moderate_tasks_nobug(id):
    task = Task.query.get_or_404(id)
    task.confirmed = True
    db.session.add(task)
    return redirect(url_for('.moderate_tasks',
                            page=request.args.get('page', 1, type=int),
                            key = request.args.get('key', '', type=str)))


@prob.route('/moderate_tasks/set_bug/<int:id>')
@login_required
@permission_required(Permission.MODERATE_TASKS)
def moderate_tasks_bug(id):
    task = Task.query.get_or_404(id)
    task.confirmed = False
    db.session.add(task)
    return redirect(url_for('.moderate_tasks',
                            page=request.args.get('page', 1, type=int),
                            key = request.args.get('key', '', type=str)))

@prob.route('/apply_suggestions/<int:id>', methods=['GET', 'POST'])
@login_required
def apply(id):
    task = Task.query.get_or_404(id)
    form = ApplyForm()
    if form.validate_on_submit():
        a = Advice(
            body = form.suggestions.data,
            author = current_user,
            task = task,
            target = task.publisher
        )
        db.session.add(a)
        db.session.commit()
        flash('您的建议已提交')
        return redirect(url_for('prob.task', id=id))
    return render_template('prob/apply_advice.html', tasks = [task], form=form)

@prob.route('/codes_for_this_task/<int:id>')
@login_required
def task_code(id):
    task = Task.query.get_or_404(id)
    if not current_user.is_viewer(task) and not current_user.is_contributor(task) and \
        not current_user.can(Permission.ADMINISTER) and current_user != task.publisher:
        current_user.score = current_user.score - task.score
        current_user.view(task)
    page = request.args.get('page', 1, type=int)
    code = Code.query.filter_by(task_id=task.id)
    if (not current_user.can(Permission.ADMINISTER)):
        code = code.filter_by(passed=True)
    pagination = code.order_by(Code.likes.desc()).order_by(Code.timestamp.desc()).paginate(
        page, per_page=current_app.config['WP_CODES_PER_PAGE'],
        error_out=False)
    codes = pagination.items
    return render_template('prob/codes_for_task.html', tasks=[task], id = id,
                               pagination=pagination, page=page, codes=codes)

@prob.route('/like_code/<int:id>')
@login_required
def like_code(id):
    page = request.args.get('page', 1, type=int)
    code = Code.query.filter_by(id=id).first()
    if code is None:
        flash('不合法的操作.')
        return redirect(url_for('prob.tasks'))
    if current_user.is_like(code):
        flash('您已为此代码点赞')
        return redirect(url_for('prob.task_code', id=code.task_id, page=page))
    current_user.like(code)
    flash('您已为 %s 的代码点赞' % code.author.username)
    return redirect(url_for('prob.task_code', id=code.task_id, page=page))


@prob.route('/unlike_code/<int:id>')
@login_required
def unlike_code(id):
    code = Code.query.filter_by(id=id).first()
    page = request.args.get('page', 1, type=int)
    if code is None:
        flash('不合法的操作.')
        return redirect(url_for('prob.tasks'))
    if not current_user.is_like(code):
        flash('您并未为此代码点赞')
        return redirect(url_for('prob.task_code', id=code.task_id, page=page))
    current_user.unlike(code)
    flash('您已取消对 %s 代码的点赞.' %  code.author.username)
    return redirect(url_for('prob.task_code', id=code.task_id, page=page))

@prob.route('/code/<int:id>')
@login_required
def code(id):
    code = Code.query.get_or_404(id)
    if (not current_user.is_solver(code.task)) and \
            (not current_user.is_viewer(code.task)) and \
            (not current_user == code.author) and \
            (not current_user.can(Permission.ADMINISTER)):
        flash('您没有权限查看此代码')
        return redirect(url_for('prob.task', id=code.task_id))
    return render_template('prob/code.html', tasks = [code.task], codes=[code])

@prob.route('/delete_code/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def delete_code(id):
    code= Code.query.get_or_404(id)
    if not current_user.can(Permission.ADMINISTER):
        abort(403)
    flash('小心！删除操作不能撤回！')
    form = SubmitCodeForm()
    if form.validate_on_submit():
        code.language = Language.query.get(form.language.data)
        code.body = form.code.data
        db.session.add(code)
        flash('代码已被更新')
        return redirect(url_for('prob.code',id = code.id))
    form.code.data=code.body
    form.language.data = code.language_id
    return render_template('prob/confirm_delete_code.html',code = code,form=form,
                           token=current_user.generate_delete_token(postid=id, expiration=3600))

@prob.route('/delete_code_confirm/<token>')
@login_required
@admin_required
def delete_code_confirm(token):
    taskid = current_user.delete_code(token)
    if taskid != -1:
        flash('代码已被删除')
        return redirect(url_for('prob.task', id = taskid))
    else:
        abort(403)

@prob.route('/code_for_task/<int:id>')
@login_required
def my_code_for_task(id):
    task = Task.query.filter_by(id=id).first()
    code = current_user.codes.filter_by(task=task)
    page = request.args.get('page', 1, type=int)
    pagination = code.order_by(Code.likes.desc()).order_by(Code.timestamp.desc()).paginate(
        page, per_page=current_app.config['WP_CODES_PER_PAGE'],
        error_out=False)
    codes = pagination.items
    return render_template('prob/my_code_for_task.html', tasks = [task], codes=codes,
                           pagination = pagination, id=id, fm=True)

@prob.route('/my_codes')
@login_required
def all_codes():
    code = current_user.codes
    page = request.args.get('page', 1, type=int)
    pagination = code.order_by(Code.timestamp.desc()).order_by(Code.likes.desc()).paginate(
        page, per_page=current_app.config['WP_CODES_PER_PAGE'],
        error_out=False)
    codes = pagination.items
    return render_template('prob/my_codes.html', codes=codes,
                           pagination = pagination, id=id, fm = True)
