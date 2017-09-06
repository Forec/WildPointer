# -*- coding: utf-8 -*-
# @Time    : 2017/9/5 19:51
# @Author  : Forec
# @File    : profile/views.py
# @Project : WildPointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn


from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from . import profile
from .forms import EditProfileForm, EditProfileAdminForm
from .. import db
from ..models import User, Role
from ..decorators import admin_required


@profile.route('/detail/<username>', methods=['GET'])
def detail(username):
    user = User.query.filter_by(username=username).first()
    return render_template('profile/detail.html', user=user)


@profile.route('/edit', methods=['GET','POST'])
@login_required
def edit():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.nickname = form.nickname.data
        current_user.contactE = form.contactE.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        db.session.commit()
        flash('您的资料已更新')
        return redirect(url_for('profile.detail', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    form.contactE.data = current_user.contactE
    return render_template('profile/edit.html', form=form)


@profile.route('/edit/<username>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(username):
    user = User.query.filter_by(username=username).first()
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
        flash('用户 ' + user.username + ' 资料已更新')
        return redirect(url_for('profile.detail', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.contactE.data = user.contactE
    form.about_me.data = user.about_me
    return render_template('profile/edit.html', form=form)