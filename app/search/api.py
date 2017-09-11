# -*- coding: utf-8 -*-
# @Time    : 2017/9/7 14:59
# @Author  : Forec
# @File    : search/api.py
# @Project : WildPointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn


from flask import request, jsonify, url_for
from sqlalchemy import text, or_
from . import sea
from ..models import Post, Question, Answer, Tag


@sea.route('/api', methods=['GET'])
@sea.route('/api/<key>', methods=['GET'])
def api_all(key=''):
    posts_with_key = Post.query.filter(or_(Post.title.like(text("'%" + key + "%'")))).all()
    questions_with_key = Question.query.filter(or_(Question.title.like(text("'%" + key + "%'")))).all()
    results = posts_with_key + questions_with_key
    results = sorted(results, key=lambda r: r.score, reverse=True)[:6]
    url_lists = []
    for result in results:
        if isinstance(result, Post):
            url_lists.append(url_for('post.detail', post_id=result.id, _external=True))
        elif isinstance(result, Question):
            url_lists.append(url_for('ques.detail', question_id=result.id, _external=True))
    return jsonify({
        'results': [result.title for result in results],
        'urls': url_lists
    })


@sea.route('/post', methods=['GET'])
@sea.route('/post/<key>', methods=['GET'])
def api_post(key=''):
    posts_with_key = Post.query.filter(or_(Post.title.like(text("'%" + key + "%'")))).order_by(Post.score.asc()).slice(0, 6)
    url_lists = []
    for result in posts_with_key:
        url_lists.append(url_for('post.detail', post_id=result.id, _external=True))
    return jsonify({
        'results': [result.title for result in posts_with_key],
        'urls': url_lists
    })


@sea.route('/question', methods=['GET'])
@sea.route('/question/<key>', methods=['GET'])
def api_question(key=''):
    questions_with_key = Question.query.filter(or_(Question.title.like(text("'%" + key + "%'")))).\
        order_by(Question.score.asc()).slice(0, 6)
    url_lists = []
    for result in questions_with_key:
        url_lists.append(url_for('ques.detail', question_id=result.id, _external=True))
    return jsonify({
        'results': [result.title for result in questions_with_key],
        'urls': url_lists
    })
