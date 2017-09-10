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
        flash('您已经成功激活了您的账户！感谢您的支持！')
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
        flash('您的账户对应的电子邮箱已经更新。')
    else:
        flash('该链接违例或已失效，请重新在 \"安全中心\" 中申请修改邮箱。')
    return redirect(url_for('profile.detail'))


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
#        if not current_user.confirmed and request.endpoint[:8] == 'comment.':
#            return redirect(url_for('auth.unconfirmed'))
