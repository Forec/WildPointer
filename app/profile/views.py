# -*- coding: utf-8 -*-
# @Time    : 2017/9/5 19:51
# @Author  : Forec
# @File    : profile/views.py
# @Project : WildPointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn


from flask import render_template, redirect, url_for, abort, flash, request, current_app
from flask_login import login_required, current_user

from . import profile
from .forms import EditProfileForm, EditProfileAdminForm
from .. import db
from ..models import User, Role, Post, Task
from ..decorators import admin_required

@profile.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    post = user.posts
    task = user.publishs

    page_post = request.args.get('page_post', 1, type=int)
    page_task = request.args.get('page_task', 1, type=int)

    pagination_post = post.order_by(Post.timestamp.desc()).paginate(
        page=page_post, per_page=current_app.config['PROFILE_WP_POSTS_PER_PAGE'],
        error_out=False
    )
    pagination_task = task.order_by(Task.timestamp.desc()).paginate(
        page=page_task, per_page=current_app.config['PROFILE_WP_TASKS_PER_PAGE'],
        error_out=False
    )
    posts = pagination_post.items
    tasks = pagination_task.items
    return render_template('main/user.html', user = user, posts= posts, tasks=tasks,
                           pagination_task = pagination_task, pagination_post=pagination_post)

@profile.route('/edit-profile', methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.contactE = form.contactE.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        db.session.commit()
        flash('您的资料已更新')
        return redirect(url_for('.user', username = current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    form.contactE.data = current_user.contactE
    return render_template('main/edit_profile.html', form=form)

@profile.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.contactE = form.contactE.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash('用户 ' + user.username +' 资料已更新')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.contactE.data = user.contactE
    form.about_me.data = user.about_me
    return render_template('main/edit_profile.html', form=form)