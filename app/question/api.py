# -*- coding: utf-8 -*-
# @Time    : 2017/9/6 16:47
# @Author  : Forec
# @File    : question/api.py
# @Project : WildPointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn

from flask import jsonify, request
from flask_login import login_required, current_user
from . import ques
from .. import db
from ..models import Question, Permission
from ..verifiers import verify_token
from ..decorators import confirm_required
import json


@ques.route('/create', methods=['POST'])
@login_required
@confirm_required
def create():
    req = request.form.get('request')
    if req is None:
        return jsonify({
            'code': 0  # 无请求
        })
    req = json.loads(req)
    title = req.get('title')
    body = '' if not req.get('body') else req.get('body')
    tags_string = '' if not req.get('tags') else req.get('tags')
    if not title:
        return jsonify({
            'code': 1   # 标题为空
        })
    invalid_tag_char = '#,.!-=+/\\`~?$%^&*()@'
    for char in invalid_tag_char:
        if tags_string.find(char) != -1:
            return jsonify({
                'code': 2  # 标签中包含不合法字符
            })
    question = Question(title=title,
                        publisher=current_user._get_current_object(),
                        body='' if body is None else body)
    db.session.add(question)
    db.session.commit()
    tag_names = [tag_string.strip() for tag_string in tags_string.split(';')]
    question.reset_tags(tag_names)
    db.session.add(question)
    db.session.commit()
    return jsonify({
        'code': 3,
        'id': question.id
    })


@ques.route('/edit/<int:question_id>', methods=['GET', 'POST'])
@login_required
def edit(question_id):
    question = Question.query.filter_by(id=question_id).first()
    if question is None:
        return jsonify({
            'code': -1  # 对应 Question 不存在
        })
    if request.method == 'GET':
        return jsonify({
            'code': 0,  # 响应数据获取请求
            'title': question.title,
            'body': question.body,
            'tags': [tag.name for tag in question.tags]
        })
    else:
        req = request.form.get('request')
        if req is None:
            return jsonify({
                'code': 1   # 没有请求
            })
        req = json.loads(req)
        email = req.get('email')
        token = req.get('token')
        title = req.get('title')
        tags = req.get('tags')
        body = req.get('body')
        user = verify_token(email, token)
        if title is None or not user or (user.id != current_user.id and not user.can(Permission.MODERATE_ALL)):
            return jsonify({
                'code': 2   # 认证失败
            })
        question.title = title
        question.body = '' if body is None else body
        question.reset_tags(tags)
        db.session.add(question)
        return jsonify({
            'code': 4       # 修改成功
        })


@ques.route('/delete', methods=['POST'])
@login_required
def delete():
    req = request.form.get('request')
    if req is None:
        return jsonify({
            'code': 1   # 没有请求
        })
    req = json.loads(req)
    question_id = req.get('question_id')
    question = Question.query.filter_by(id=question_id).first()
    if question is None:
        return jsonify({
            'code': -1  # 对应 Question 不存在
        })
    email = req.get('email')
    token = req.get('token')
    user = verify_token(email, token)
    if not user:
        return jsonify({
            'code': 2   # 认证失败
        })
    user.delete_question(question_id)
    db.session.delete(question)
    return jsonify({
        'code': 3       # 删除成功
    })


@ques.route('/like/<int:question_id>', methods=['GET'])
@login_required
def like(question_id):
    question = Question.query.filter_by(id=question_id).first()
    if question is None:
        return jsonify({
            'code': -1  # 对应 Question 不存在
        })
    if current_user.is_like_question(question):
        current_user.cancel_like_question(question)
        return jsonify({
            'code': 0   # 已取消点赞
        })
    current_user.like_question(question)
    return jsonify({
        'code': 1,
        'score': question.score
    })


@ques.route('/unlike/<int:question_id>', methods=['GET'])
@login_required
def unlike(question_id):
    question = Question.query.filter_by(id=question_id).first()
    if question is None:
        return jsonify({
            'code': -1  # 对应 Question 不存在
        })
    if current_user.is_unlike_question(question):
        current_user.cancel_unlike_question(question)
        return jsonify({
            'code': 0   # 已取消反对
        })
    current_user.unlike_question(question)
    return jsonify({
        'code': 1,
        'score': question.score
    })
