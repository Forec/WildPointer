# -*- coding: utf-8 -*-
# @Time    : 2017/9/7 15:07
# @Author  : Forec
# @File    : search/views.py
# @Project : WildPointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn


from flask import request, flash, render_template, redirect, url_for
from sqlalchemy import or_, text
from . import sea
from ..models import Post, Question, Answer, Tag


@sea.route('/<key>')
def home(key):
    key_list = list(filter(lambda x: len(x) > 0, [k.strip() for k in key.split(' ')]))
    if not key_list:
        flash('您未输入任何有效关键词')
        return redirect(url_for('main.index', _external=True))
    post_only = request.args.get('post_only', 0, type=int)
    question_only = request.args.get('question_only', 0, type=int)
    posts = Post.query
    questions = Question.query
    answers = Answer.query
    tag_set = set([])
    for key in key_list:
        tag_set |= set(Tag.query.filter_by(name=key).all())
    tag_list = list(tag_set)
    if post_only != 0:
        posts = []
    else:
        fk = key_list[0]
        post_with_key = set(posts.filter(or_(Post.title.like(text("'%"+fk+"%'")),
                                             Post.body.like(text("'%"+fk+"%'")))).all())
        for k in key_list[1:]:
            sub_posts = posts.filter(or_(Post.title.like(text("'%"+k+"%'")),
                                         Post.body.like(text("'%"+k+"%'")))).all()
            post_with_key |= set(sub_posts)
        post_with_tag = set([tag.posts for tag in tag_list])
        posts = list(post_with_key | post_with_tag)
    if question_only != 0:
        answers = []
        questions = []
    else:
        fk = key_list[0]
        ques_with_key = set(questions.filter(or_(Question.title.like(text("'%"+fk+"%'")),
                                                 Question.body.like(text("'%"+fk+"%'")))).all())
        anss_with_key = set(answers.filter(Answer.body.like(text("'%"+fk+"%'"))).all())
        for k in key_list[1:]:
            sub_questions = questions.filter(or_(Question.title.like(text("'%"+k+"%'")),
                                                 Question.body.like(text("'%"+k+"%'")))).all()
            sub_answers = answers.filter(Answer.body.like(text("'%"+k+"%'"))).all()
            ques_with_key |= set(sub_questions)
            anss_with_key |= set(sub_answers)
        ques_with_tag = set([tag.questions for tag in tag_list])
        questions = list(ques_with_key | ques_with_tag)
        answers = list(anss_with_key)
    results = posts + questions + answers
    results = sorted(results, key=lambda r: r.score, reverse=True)

    return render_template('search/result.html', results=results)
