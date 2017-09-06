# -*- coding: utf-8 -*-
# @Time    : 2017/9/6 19:36
# @Author  : Forec
# @File    : answer/views.py
# @Project : WildPointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn


from flask import render_template, request, current_app
from flask_login import login_required, current_user
from . import ans
from ..models import Answer


@ans.route('/me')
@login_required
def me():
    page = request.args.get('page', 1, type=int)
    pagination = current_user.answers.order_by(Answer.timestamp.desc()).paginate(
        page, per_page=current_app.config['WP_ANSWERS_PER_PAGE'],
        error_out=False)
    answers = pagination.items
    return render_template('answer/me.html', answers=answers, pagination=pagination)
