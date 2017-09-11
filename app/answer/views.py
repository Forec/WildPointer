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
from ..decorators import confirm_required


@ans.route('/me', methods=['GET'])
@login_required
@confirm_required
def me():
    page = request.args.get('page', 1, type=int)
    pagination = current_user.answers.order_by(Answer.last_edit.desc()).paginate(
        page, per_page=int(current_app.config['WP_ANSWERS_PER_PAGE'] * 1.6),
        error_out=False)
    answers = pagination.items
    answer_count = int(len(answers) / 2) if len(answers) % 2 == 0 else int(len(answers) / 2) + 1
    answers_1 = answers[:answer_count]
    answers_2 = answers[answer_count:]
    return render_template('answer/me.html', answers_1=answers_1,
                           answers_2=answers_2, pagination=pagination)


@ans.route('/user/<int:user_id>', methods=['GET'])
def user(user_id):
    from ..models import User
    user = User.query.get_or_404(user_id)
    page = request.args.get('page', 1, type=int)
    pagination = user.answers.order_by(Answer.last_edit.desc()).paginate(
        page, per_page=int(current_app.config['WP_ANSWERS_PER_PAGE'] * 1.6),
        error_out=False)
    answers = pagination.items
    answer_count = int(len(answers) / 2) if len(answers) % 2 == 0 else int(len(answers) / 2) + 1
    answers_1 = answers[:answer_count]
    answers_2 = answers[answer_count:]
    return render_template('answer/user.html', answers_1=answers_1, user=user,
                           answers_2=answers_2, pagination=pagination)
