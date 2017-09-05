# -*- coding: utf-8 -*-
# @Time    : 2017/9/5 19:21
# @Author  : Forec
# @File    : auth/views.py
# @Software: Wild-Pointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn

from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, logout_user, current_user

from .forms import ChangePasswordForm, ChangeEmailForm, PasswordResetForm, PasswordResetRequestForm
from . import auth
from .. import db
from ..models import User
from ..email import send_email


@auth.route('/rules')
def rules():
    return render_template('auth/rules.html')

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已经登出')
    return redirect(url_for('main.index'))

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index', _external=True))
    if current_user.confirm(token):
        flash('您已经验证了您的邮箱！感谢您的支持！')
    else:
        flash('此验证链接无效或已过期！')
    return redirect(url_for('main.index', _external=True))

@auth.route('/resend_confirmation')
@login_required
def resend_confirmation():
    if current_user.confirmed:
        flash('您的账号已经激活，无需重新验证！')
        return redirect(url_for('main.index', _external=True))
    token = current_user.generate_confirmation_token()
    send_email(current_user.email,
               '确认您的帐户',
               'auth/email/confirm',
               user = current_user,
               token = token)
    flash('一封确认邮件已经发送到您注册时填写的邮箱，'
          '请查看以激活您的帐号')
    return redirect(url_for('main.index', _external=True))

@auth.route('/change-password', methods=['GET','POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.oldPassword.data):
            current_user.password = form.newPassword.data
            db.session.add(current_user)
            db.session.commit()
            flash('您的密码已更新')
            return redirect(url_for('main.index'))
        else:
            flash('密码错误')
    return render_template('auth/change_password.html', form = form)

@auth.route('/change-email', methods = ['GET', 'POST'])
@login_required
def change_email_request():
    form =ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data
            token = current_user.generate_email_change_token(new_email)
            send_email(new_email, '确认您的邮箱',
                       'auth/email/change_email',
                       user = current_user, token = token)
            flash('一封包含指导您激活新邮箱的邮件已经发到您的新邮箱')
            return redirect(url_for('main.index'))
        else:
            flash('错误的的用户名或密码')
    return render_template("auth/change_email.html", form=form)

@auth.route('/change-email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        flash('您的电子邮箱已经更新')
    else:
        flash('非法请求')
    return redirect(url_for('main.index'))


@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email,'重置您的密码',
                       'auth/email/reset_password',
                       user = user, token = token,
                       next = request.args.get('next'))
            flash('一封指导您重置密码的邮件已经发送到您注册时填写的邮箱，请'
              '查看邮件并重置您的密码')
            return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)

@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            return redirect(url_for('main.index'))
        if user.reset_password(token, form.password.data):
            flash('您的密码已经重置成功')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)

@auth.route('/secure_center')
@login_required
def secure_center():
    return render_template('auth/secure_center.html')

@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
                and request.endpoint[:5] != 'auth.' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))
