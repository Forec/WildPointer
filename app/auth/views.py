# -*- coding: utf-8 -*-
# @Time    : 2017/9/5 19:21
# @Author  : Forec
# @File    : auth/views.py
# @Software: Wild-Pointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn

from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, logout_user, current_user
from .forms import PasswordResetForm, PasswordResetRequestForm
from . import auth
from ..models import User
from ..email import send_email


@auth.route('/rules', methods=['GET'])
def rules():
    return render_template('auth/rules.html')


@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash('您已成功登出')
    return redirect(url_for('main.index'))


@auth.route('/confirm/<token>', methods=['GET'])
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index', _external=True))
    if current_user.confirm(token):
        flash('您已经验证了您的邮箱！感谢您的支持！')
    else:
        flash('此验证链接无效或已过期！')
    return redirect(url_for('main.index', _external=True))


@auth.route('/secure', methods=['GET'])
@login_required
def secure():
    return render_template('auth/secure.html')


@auth.route('/change-email/<token>', methods=['GET'])
@login_required
def change_email(token):
    if current_user.change_email(token):
        flash('您的电子邮箱已经更新')
    else:
        flash('非法请求')
    return redirect(url_for('profile.detail'))


@auth.route('/reset', methods=['GET', 'POST'])
def forget_password():
    if not current_user.is_anonymous:
        flash('您已经登陆，请在 "安全中心" 修改密码')
        return redirect(url_for('auth.secure', _external=True))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, '重置您的密码', 'auth/email/reset_password', user=user, token=token,
                       next=request.args.get('next'))
            flash('一封指导您重置密码的邮件已经发送到您注册时填写的邮箱，请查看邮件并重置您的密码')
            return redirect(url_for('auth.login'))
    return render_template('auth/forget.html', form=form)


@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        flash('您已经登陆，请在 "安全中心" 修改密码')
        return redirect(url_for('auth.secure', _external=True))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            flash('此链接已失效')
            return redirect(url_for('main.index'))
        if user.reset_password(token, form.password.data):
            flash('您的密码已经重置成功')
            return redirect(url_for('auth.login'))
        else:
            flash('此链接已失效')
            return redirect(url_for('main.index'))
    return render_template('auth/reset.html', form=form)


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed and request.endpoint[:8] == 'comment.':
            return redirect(url_for('auth.unconfirmed'))
