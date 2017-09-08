# -*- coding: utf-8 -*-
# @Time    : 2017/9/6 18:58
# @Author  : Forec
# @File    : answer/api.py
# @Project : WildPointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn


from flask import jsonify, request
from flask_login import login_required, current_user
from sqlalchemy import and_
from . import ans
from .. import db
from ..models import Permission, Answer, Question
from ..verifiers import verify_token
import json


@ans.route('/detail/<int:answer_id>', methods=['GET'])
def detail(answer_id):
    answer = Answer.query.filter_by(id=answer_id).first()
    if answer is None:
        return jsonify({
            'code': -1  # 不存在对应 Answer
        })
    return jsonify({
        'code': 0,
        'author_id': answer.author_id,
        'author_nickname': answer.author.nickname,
        'content': answer.body,
        'score': answer.score,
        'create_timestamp': answer.timestamp
    })


@ans.route('/create', methods=['POST'])
@login_required
def create():
    req = request.form.get('request')
    if req is None:
        return jsonify({
            'code': -1  # 无请求
        })
    req = json.loads(req)
    [email, token, body, question_id] = [req.get(name) for name in ['email', 'token', 'body', 'question_id']]
    user = verify_token(email, token)
    if not type or not body or not user or user.id != current_user.id:
        return jsonify({
            'code': 0  # 参数格式不正确／用户不存在／认证失败
        })
    try:
        question_id = int(question_id)
    except ValueError:
        return jsonify({
            'code': 0
        })
    answer = Answer.query.filter_by(and_(author_id=user.id, question_id=question_id)).first()
    if answer:
        return jsonify({
            'code': 1,  # 已有回答
            'answer_id': answer.id
        })
    question = Question.query.filter_by(id=question_id).first()
    if not question:
        return jsonify({
            'code': 2   # 问题不存在
        })
    answer = Answer(question=question, author=user, body=body)
    db.session.add(answer)
    return jsonify({
        'code': 3,
        'id': answer.id
    })


@ans.route('/delete/<int:answer_id>', methods=['GET'])
@login_required
def delete(answer_id):
    answer = Answer.query.filter_by(id=answer_id).first()
    if not answer:
        return jsonify({
            'code': -1  # 不存在对应 Answer
        })
    if current_user.id != answer.author_id and not current_user.can(Permission.MODERATE_ALL):
        return jsonify({
            'code': 0   # 无操作权限
        })
    if current_user.delete_answer(answer_id):
        return jsonify({
            'code': 1   # 删除成功
        })
    else:
        return jsonify({
            'code': 2   # 未知错误
        })
