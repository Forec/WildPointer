# -*- coding: utf-8 -*-
# @Time    : 2017/9/5 16:42
# @Author  : Forec
# @File    : question/views.py
# @Project : WildPointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn


from flask import render_template, request, current_app
from . import ques
from ..models import Question, Answer


@ques.route('/latest', methods=['GET'])
def latest_questions():
    page = request.args.get('page', 1, type=int)
    pagination = Question.query.order_by(Question.timestamp.desc()).paginate(
        page, per_page=current_app.config['WP_QUESTIONS_PER_PAGE'],
        error_out=False
    )
    questions = pagination.items
    return render_template('question/home.html', questions=questions, pagination=pagination)


@ques.route('/<int:question_id>', methods=['GET'])
def detail(question_id):
    question = Question.query.filter_by(id=question_id).first()
    page = request.args.get('page', 1, type=int)
    pagination = question.answers.order_by(Answer.score.asc()).paginate(
        page, per_page=current_app.config['WP_COMMENTS_PER_PAGE'],
        error_out=False
    )
    answers = pagination.items
    return render_template('question/question.html',
                           question=question,
                           answers=answers,
                           pagination=pagination)
