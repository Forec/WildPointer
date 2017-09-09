# -*- coding: utf-8 -*-
# @Time    : 2017/9/5 16:42
# @Author  : Forec
# @File    : question/views.py
# @Project : WildPointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn


from flask import render_template, request, current_app
from flask_login import login_required, current_user
from . import ques
from ..models import Question, Answer


@ques.route('/latest', methods=['GET'])
def latest():
    page = request.args.get('page', 1, type=int)
    pagination = Question.query.order_by(Question.create.desc()).paginate(
        page, per_page=current_app.config['WP_QUESTIONS_PER_PAGE'],
        error_out=False
    )
    questions = pagination.items
    hot_questions = Question.query.order_by(Question.score.asc()).slice(0, 6).all()
    return render_template('question/latest.html', questions=questions, pagination=pagination,
                           hot_questions=hot_questions)


@ques.route('/<int:question_id>', methods=['GET'])
def detail(question_id):
    question = Question.query.filter_by(id=question_id).first()
    page = request.args.get('page', 1, type=int)
    pagination = question.answers.order_by(Answer.score.asc()).paginate(
        page, per_page=current_app.config['WP_ANSWERS_PER_PAGE'],
        error_out=False
    )
    answers = pagination.items
    return render_template('question/question.html',
                           question=question,
                           answers=answers,
                           pagination=pagination)


@ques.route('/me', methods=['GET'])
@login_required
def me():
    query = Question.query.filter_by(publisher_id=current_user.id)
    page = request.args.get('page', 1, type=int)
    pagination = query.order_by(Question.last_edit.desc()).paginate(
        page, per_page=int(current_app.config['WP_QUESTIONS_PER_PAGE'] * 1.2),
        error_out=False
    )
    questions = pagination.items
    question_count = int(len(questions) / 2) if len(questions) % 2 == 0 else int(len(questions) / 2) + 1
    questions_1 = questions[:question_count]
    questions_2 = questions[question_count:]
    return render_template('question/me.html', questions_1=questions_1,
                           questions_2=questions_2, pagination=pagination)
