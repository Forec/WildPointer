# -*- coding: utf-8 -*-
# @Time    : 2017/9/7 15:07
# @Author  : Forec
# @File    : search/views.py
# @Project : WildPointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn


from flask import request, flash, render_template, redirect, url_for, current_app
from sqlalchemy import or_, text
from . import sea
from ..models import Post, Question, Answer, Tag, Pagination


@sea.route('/', methods=['GET'])
@sea.route('/<key>', methods=['GET'])
def home(key=''):
    key_list = list(filter(lambda x: len(x) > 0, [k.strip() for k in key.split(' ')]))
    page = request.args.get('page', 1, type=int)
    post_only = request.args.get('post_only', 0, type=int)
    question_only = request.args.get('question_only', 0, type=int)
    specified_tags = request.args.get('tags', '')
    hot_tags = Tag.query.order_by(Tag.count.asc()).slice(0, 20).all()
    if not key_list:
        key_list = ['']
    if specified_tags:
        specified_tags = list(filter(lambda x: x.strip() != '', specified_tags.split(';')))
        tag_list = list(filter(lambda x: x is not None, [Tag.query.filter_by(name=t).first() for t in specified_tags]))
        if tag_list:
            posts = []
            satisfy_posts = []
            if question_only == 0:
                for tag in tag_list:
                    posts.extend(tag.get_posts().all())
                for _post in posts:
                    for keyword in key_list:
                        if _post.title.find(keyword) != -1 or _post.body.find(keyword) != -1:
                            satisfy_posts.append(_post)
                            break
            questions = []
            satisfy_questions = []
            if post_only == 0:
                for tag in tag_list:
                    questions.extend(tag.get_questions().all())
                for _question in questions:
                    for keyword in key_list:
                        if _question.title.find(keyword) != -1 or _question.body.find(keyword) != -1:
                            satisfy_questions.append(_question)
            results = satisfy_posts + satisfy_questions
            results = sorted(results, key=lambda r: r.score, reverse=True)
            pagination = Pagination(page=page, per_page=current_app.config['WP_RESULTS_PER_PAGE'],
                                    total_count=len(results))
            return render_template('search/result.html', title=key, results=results, pagination=pagination,
                                   tags=list(set(hot_tags)-set(tag_list)), used_tags=tag_list, type='all')
        return render_template('search/result.html', title=key, results=[], pagination=None,
                               tags=list(set(hot_tags)-set(tag_list)), used_tags=tag_list, type='all')
    posts = Post.query
    questions = Question.query
    answers = Answer.query
    tag_set = set([])
    for key in key_list:
        tag_set |= set(Tag.query.filter_by(name=key).all())
    tag_list = list(tag_set)
    if question_only != 0:
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
    if post_only != 0:
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
    pagination = Pagination(page=page, per_page=current_app.config['WP_RESULTS_PER_PAGE'], total_count=len(results))
    return render_template('search/result.html', title=key, results=results, pagination=pagination,
                           tags=hot_tags, used_tags=[], type='all')


@sea.route('/post', methods=['GET'])
@sea.route('/post/<key>', methods=['GET'])
def post(key=''):
    key_list = list(filter(lambda x: len(x) > 0, [k.strip() for k in key.split(' ')]))
    page = request.args.get('page', 1, type=int)
    posts = Post.query
    specified_tags = request.args.get('tags', '')
    hot_tags = Tag.query.order_by(Tag.count.asc()).slice(0, 20).all()
    if not key_list:
        key_list = ['']
    if specified_tags:
        specified_tags = list(filter(lambda x: x.strip() != '', specified_tags.split(';')))
        tag_list = list(filter(lambda x: x is not None, [Tag.query.filter_by(name=t).first() for t in specified_tags]))
        if tag_list:
            posts = []
            satisfy_posts = []
            for tag in tag_list:
                posts.extend(tag.get_posts().all())
            for _post in posts:
                for keyword in key_list:
                    if _post.title.find(keyword) != -1 or _post.body.find(keyword) != -1:
                        satisfy_posts.append(_post)
                        break
            results = satisfy_posts
            results = sorted(results, key=lambda r: r.score, reverse=True)
            pagination = Pagination(page=page, per_page=current_app.config['WP_RESULTS_PER_PAGE'],
                                    total_count=len(results))
            return render_template('search/post.html', title=key, results=results, pagination=pagination,
                                   tags=list(set(hot_tags)-set(tag_list)), used_tags=tag_list, type='post')
        return render_template('search/post.html', title=key, results=[], pagination=None,
                               tags=list(set(hot_tags)-set(tag_list)), used_tags=tag_list, type='post')
    tag_set = set([])
    for key in key_list:
        tag_set |= set(Tag.query.filter_by(name=key).all())
    tag_list = list(tag_set)
    fk = key_list[0]
    post_with_key = set(posts.filter(or_(Post.title.like(text("'%"+fk+"%'")),
                                         Post.body.like(text("'%"+fk+"%'")))).all())
    for k in key_list[1:]:
        sub_posts = posts.filter(or_(Post.title.like(text("'%"+k+"%'")),
                                     Post.body.like(text("'%"+k+"%'")))).all()
        post_with_key |= set(sub_posts)
    post_with_tag = set([tag.posts for tag in tag_list])
    posts = list(post_with_key | post_with_tag)
    results = posts
    results = sorted(results, key=lambda r: r.score, reverse=True)

    pagination = Pagination(page=page, per_page=current_app.config['WP_RESULTS_PER_PAGE'], total_count=len(results))

    return render_template('search/post.html', title=key, results=results, pagination=pagination, type='post',
                           tags=hot_tags, used_tags=[])


@sea.route('/question', methods=['GET'])
@sea.route('/question/<key>', methods=['GET'])
def question(key=''):
    key_list = list(filter(lambda x: len(x) > 0, [k.strip() for k in key.split(' ')]))
    page = request.args.get('page', 1, type=int)
    questions = Question.query
    specified_tags = request.args.get('tags', '')
    hot_tags = Tag.query.order_by(Tag.count.asc()).slice(0, 20).all()
    if not key_list:
        key_list = ['']
    if specified_tags:
        specified_tags = list(filter(lambda x: x.strip() != '', specified_tags.split(';')))
        tag_list = list(filter(lambda x: x is not None, [Tag.query.filter_by(name=t).first() for t in specified_tags]))
        if tag_list:
            questions = []
            satisfy_questions = []
            for tag in tag_list:
                questions.extend(tag.get_questions().all())
            for _question in questions:
                for keyword in key_list:
                    if _question.title.find(keyword) != -1 or _question.body.find(keyword) != -1:
                        satisfy_questions.append(_question)
            results = satisfy_questions
            results = sorted(results, key=lambda r: r.score, reverse=True)
            pagination = Pagination(page=page, per_page=current_app.config['WP_RESULTS_PER_PAGE'],
                                    total_count=len(results))
            return render_template('search/question.html', title=key, results=results, pagination=pagination,
                                   tags=list(set(hot_tags)-set(tag_list)), used_tags=tag_list, type='question')
        return render_template('search/question.html', title=key, results=[], pagination=None,
                               tags=list(set(hot_tags)-set(tag_list)), used_tags=tag_list, type='question')
    answers = Answer.query
    tag_set = set([])
    for key in key_list:
        tag_set |= set(Tag.query.filter_by(name=key).all())
    tag_list = list(tag_set)
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
    results = questions + answers
    results = sorted(results, key=lambda r: r.score, reverse=True)

    pagination = Pagination(page=page, per_page=current_app.config['WP_RESULTS_PER_PAGE'], total_count=len(results))

    return render_template('search/question.html', title=key, results=results, pagination=pagination, type='question',
                           tags=hot_tags, used_tags=[])
