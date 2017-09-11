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
from ..models import Question, Answer, Permission, Tag


@ques.route('/latest', methods=['GET'])
def latest():
    page = request.args.get('page', 1, type=int)
    pagination = Question.query.order_by(Question.create.desc()).paginate(
        page, per_page=current_app.config['WP_QUESTIONS_PER_PAGE'],
        error_out=False
    )
    questions = pagination.items
    hot_questions = Question.query.order_by(Question.score.asc()).slice(0, 6).all()
    hot_tags = Tag.query.order_by(Tag.count.asc()).slice(0, 16).all()
    return render_template('question/latest.html', questions=questions, pagination=pagination,
                           hot_questions=hot_questions,
                           tags=hot_tags, used_tags=[], type='question')


@ques.route('/<int:question_id>', methods=['GET'])
def detail(question_id):
    question = Question.query.get_or_404(question_id)
    page = request.args.get('page', 1, type=int)
    pagination = question.answers.order_by(Answer.score.asc()).paginate(
        page, per_page=current_app.config['WP_ANSWERS_PER_PAGE'],
        error_out=False
    )
    moderate = current_user.can(Permission.MODERATE_ALL)
    answers = pagination.items
    has_liked = False if not current_user.is_authenticated else \
        current_user.confirmed and current_user.is_like_question(question)
    has_unliked = False if not current_user.is_authenticated else \
        current_user.confirmed and current_user.is_unlike_question(question)
    recent_questions = question.publisher.questions.order_by(Question.last_edit.desc()).slice(0, 5).all()
    for i in range(0, len(recent_questions)):
        if recent_questions[i].id == question.id:
            recent_questions = recent_questions[:i] + recent_questions[i+1:]
            break
    tags = [item.tag for item in question.tags.all()]
    return render_template('question/detail.html',
                           question=question,
                           answers=answers,
                           moderate=moderate,
                           tags=tags,
                           pagination=pagination,
                           has_liked=has_liked,
                           has_unliked=has_unliked,
                           recent_questions=recent_questions)


@ques.route('/me', methods=['GET'])
@login_required
def me():
    query = current_user.questions
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


@ques.route('/user/<int:user_id>', methods=['GET'])
def user(user_id):
    from ..models import User
    user = User.query.get_or_404(user_id)
    query = user.questions
    page = request.args.get('page', 1, type=int)
    pagination = query.order_by(Question.last_edit.desc()).paginate(
        page, per_page=int(current_app.config['WP_QUESTIONS_PER_PAGE'] * 1.2),
        error_out=False
    )
    questions = pagination.items
    question_count = int(len(questions) / 2) if len(questions) % 2 == 0 else int(len(questions) / 2) + 1
    questions_1 = questions[:question_count]
    questions_2 = questions[question_count:]
    return render_template('question/user.html', questions_1=questions_1, user=user,
                           questions_2=questions_2, pagination=pagination)
