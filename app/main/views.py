# -*- coding: utf-8 -*-
# @Time    : 2017/9/5 09:52
# @Author  : Forec
# @File    : main/views.py
# @Project : WildPointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn


from flask import render_template, redirect, url_for, abort, flash, request, current_app, make_response
from flask_login import login_required, current_user
from sqlalchemy import or_

from . import main
from .forms import HomeForm, CommentForm, SearchForm, EditApplyForm
from .. import db
from ..models import Permission, Post, Comment, Advice
from ..decorators import permission_required


@main.route('/', methods=['GET', 'POST'])
def index():
    form = HomeForm()
    if current_user.can(Permission.WRITE_ARTICLES) and \
        form.validate_on_submit():
        if form.title.data == '' or form.title.data is None:
            form.title.data = "Untitled"
        post = Post(title = form.title.data,
                    body = form.body.data,
                    author = current_user._get_current_object())
        db.session.add(post)
        # db.session.commit()
        return redirect(url_for('.index'))
    show_followed = False
    if current_user.is_authenticated:
        show_followed = bool(request.cookies.get('show_followed', ''))
    if show_followed:
        query = current_user.followed_posts
    else:
        query = Post.query
    page = request.args.get('page', 1, type=int)
    pagination = query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['WP_POSTS_PER_PAGE'],
        error_out=False
    )
    posts = pagination.items
    return render_template('index.html', form=form, posts=posts,
                           pagination=pagination, show_followed=show_followed)


@main.route('/all')
@login_required
def show_all():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '', max_age=30*24*60*60)
    return resp


@main.route('/followed')
@login_required
def show_followed():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '1', max_age=30*24*60*60)
    return resp


@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.get_or_404(id)
    form =CommentForm()
    if form.validate_on_submit():
        comment = Comment(body = form.body.data,
                          post = post,
                          author = current_user._get_current_object())
        db.session.add(comment)
        flash('您的评论已发布')
        return redirect(url_for('.post', id=post.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1)// \
            current_app.config['WP_COMMENTS_PER_PAGE'] + 1
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=current_app.config['WP_COMMENTS_PER_PAGE'],
        error_out=False
    )
    comments = pagination.items
    return render_template('main/post.html', posts=[post], comments = comments,
                           pagination = pagination, post = post, form = form,
                           moderate=current_user.can(Permission.MODERATE_COMMENTS))


@main.route('/edit/<int:id>', methods=['GET','POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and \
        not current_user.can(Permission.ADMINISTER):
        abort(403)
    form = HomeForm()
    if form.validate_on_submit():
        if form.title.data == '' or form.title.data is None:
            form.title.data = 'Untitled'
        post.title = form.title.data
        post.body = form.body.data
        db.session.add(post)
        db.session.commit()
        flash('文章已更新')
        return redirect(url_for('.post', id=post.id))
    form.body.data = post.body
    form.title.data = post.title
    return render_template('main/edit_post.html', form = form)



@main.route('/delete-post/<int:id>', methods=['GET','POST'])
@login_required
def delete_post(id):
    post= Post.query.get_or_404(id)
    if current_user != post.author and not current_user.can(Permission.ADMINISTER):
        abort(403)
    flash('小心！删除操作不能撤回！')
    form = HomeForm()
    if form.validate_on_submit():
        if form.title.data == '' or form.title.data is None:
            form.title.data = 'Untitled'
        post.title = form.title.data
        post.body = form.body.data
        db.session.add(post)
        flash('文章已被更新')
        return redirect(url_for('.post',id = post.id))
    form.body.data=post.body
    form.title.data = post.title
    return render_template('main/confirm_delete_post.html',post = post,form=form, token=current_user.generate_delete_token(postid=id, expiration=3600))


@main.route('/delete-post-confirm/<token>')
@login_required
def delete_post_confirm(token):
    if current_user.delete_post(token):
        flash('文章已被删除')
        return redirect(url_for('main.index'))
    else:
        abort(403)


@main.route('/rules')
def rules():
    return render_template('main/rules.html')


@main.route('/moderate_comments', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_comments():
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for('main.moderate_comments', key=form.key.data))
    page = request.args.get('page', 1, type=int)
    key = request.args.get('key', '', type=str)
    if key == '':
        comment = Comment.query
    else:
        comment = Comment.query.filter(Comment.body.like('%'+key+'%'))
    pagination = comment.order_by(Comment.timestamp.desc()).paginate(
        page, per_page=current_app.config['WP_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    form.key.data = key
    return render_template('main/moderate_comments.html', comments=comments,
                           pagination=pagination, page=page, form=form)


@main.route('/moderate_comments/enable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_comments_enable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = False
    db.session.add(comment)
    return redirect(url_for('.moderate_comments',
                            page=request.args.get('page', 1, type=int)))


@main.route('/moderate_comments/disable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_comments_disable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = True
    db.session.add(comment)
    return redirect(url_for('.moderate_comments',
                            page=request.args.get('page', 1, type=int)))


@main.route('/moderate_comments/disable_own/<int:id>')
@login_required
def moderate_comments_disable_own(id):
    comment = Comment.query.get_or_404(id)
    if comment.author == current_user or comment.post.author == current_user:
        comment.disabled = True
        db.session.add(comment)
        flash('评论已被设置为不可见')
        return redirect(url_for('.post', id = comment.post_id))


@main.route('/moderate_posts', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_posts():
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for('main.moderate_posts', key=form.key.data))
    page = request.args.get('page', 1, type=int)
    key = request.args.get('key', '', type=str)
    if key == '':
        post = Post.query
    else:
        post = Post.query.filter(or_(Post.title.like('%'+key+'%'),Post.body.like('%'+key+'%')))
    pagination = post.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['WP_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    form.key.data = key
    return render_template('main/moderate_posts.html', posts=posts,
                           pagination=pagination, page=page, form=form)

@main.route('/moderate_posts/enable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_posts_enable(id):
    post = Post.query.get_or_404(id)
    post.disabled = False
    db.session.add(post)
    return redirect(url_for('.moderate_posts',
                            page=request.args.get('page', 1, type=int),
                            key = request.args.get('key', '', type=str)))


@main.route('/moderate_posts/disable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_posts_disable(id):
    post = Post.query.get_or_404(id)
    post.disabled = True
    db.session.add(post)
    return redirect(url_for('.moderate_posts',
                            page=request.args.get('page', 1, type=int),
                            key = request.args.get('key', '', type=str)))

@main.route('/messages/')
@login_required
def message():
    uncheck_messages = current_user.messages.order_by(Advice.viewed.asc()).\
        order_by(Advice.timestamp.desc())
    page = request.args.get('page', 1, type=int)
    pagination = uncheck_messages.paginate(
        page, per_page=current_app.config['WP_ADVICES_PER_PAGE'],
        error_out=False
    )
    cur_messages = pagination.items
    return render_template('main/message.html', messages = cur_messages,
                           pagination = pagination)

@main.route('/edit-advice/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_advice(id):
    advice = Advice.query.get_or_404(id)
    task = advice.task
    if current_user != advice.author and \
        not current_user.can(Permission.ADMINISTER):
        abort(403)
    form = EditApplyForm()
    if form.validate_on_submit():
        advice.body = form.suggestions.data
        db.session.add(advice)
        db.session.commit()
        flash('建议已更新')
        return redirect(url_for('main.advice', id=advice.id))
    form.suggestions.data = advice.body
    return render_template('main/edit_advice.html', form = form, tasks=[task])

@main.route('/delete-advice/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_advice(id):
    advice= Advice.query.get_or_404(id)
    task = advice.task
    if (not current_user.can(Permission.ADMINISTER)) and (current_user != advice.author):
        abort(403)
    flash('小心！删除操作不能撤回！')
    form = EditApplyForm()
    if form.validate_on_submit():
        advice.body = form.suggestions.data
        db.session.add(advice)
        flash('建议已被更新')
        return redirect(url_for('main.advice',id = advice.id))
    form.suggestions.data=advice.body
    return render_template('main/confirm_delete_advice.html',tasks=[task],form=form,
                           token=current_user.generate_delete_token(postid=id, expiration=3600))

@main.route('/delete-advice-confirm/<token>')
@login_required
def delete_advice_confirm(token):
    taskid =  current_user.delete_advice(token)
    if taskid != -1:
        flash('建议已被删除')
        return redirect(url_for('prob.task', id=taskid))
    else:
        abort(403)

@main.route('/advice/<int:id>')
def advice(id):
    advice= Advice.query.get_or_404(id)
    task = advice.task
    return render_template('main/single_advice.html',tasks=[task],advices=[advice])

@main.route('/accept-advice/<int:id>')
@login_required
def accept_advice(id):
    advice = Advice.query.filter_by(id=id).first()
    author = advice.author
    task = advice.task
    if current_user == task.publisher or current_user.can(Permission.ADMINISTER):
        advice.accept = True
        advice.viewed = True
        advice.close = False
        author.contribute(task)
        flash('建议已采纳')
        # TODO call author of advice
        if current_user.messages.filter_by(viewed=False).first() is None:
            return redirect(url_for('prob.task', id = task.id))
        else:
            return redirect(url_for('main.message'))
    else:
        abort(403)


@main.route('/close-advice/<int:id>')
@login_required
def close_advice(id):
    advice = Advice.query.filter_by(id=id).first()
    author = advice.author
    task = advice.task
    if current_user == task.publisher or current_user.can(Permission.ADMINISTER):
        advice.accept = False
        advice.viewed = True
        advice.close = True
        flash('建议已关闭')
        # TODO call author of advice

        if current_user.messages.filter_by(viewed=False).first() is None:
            return redirect(url_for('prob.task', id = task.id))
        else:
            return redirect(url_for('main.message'))
    else:
        abort(403)

@main.route('/reply-advice/<int:id>')
@login_required
def reply_advice(id):
    # TODO
    pass

