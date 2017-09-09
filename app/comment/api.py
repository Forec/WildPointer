# -*- coding: utf-8 -*-
# @Time    : 2017/9/7 00:11
# @Author  : Forec
# @File    : comment/views.py
# @Project : WildPointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn

from flask import jsonify, request
from flask_login import login_required, current_user
from . import comment as comm
from ..models import PostComment, QuestionComment, AnswerComment, comment_table, material_table
from .. import db
from ..verifiers import verify_token
import json


@comm.route('/create', methods=['POST'])
@login_required
def create():
    req = request.form.get('request')
    if req is None:
        return jsonify({
        'code': -1  # 无请求
        })
    req = json.loads(req)
    [email, token, body, parent_id, type] = [req.get(name) for name in ['email', 'token', 'body', 'parent_id', 'type']]
    user = verify_token(email, token)
    if not type or not body or not user or user.id != current_user.id:
        return jsonify({
            'code': 0  # 参数格式不正确／用户不存在／认证失败
        })
    try:
        parent_id = int(parent_id)
    except ValueError:
        return jsonify({
            'code': 0
        })
    parent = material_table.get(type).query.filter_by(id=parent_id)
    if not parent:
        return jsonify({
            'code': 1
        })
    comment = comment_table.get(type)(body=body, parent=parent)
    db.session.add(comment)
    return jsonify({
        'code': 1,
        'id': comment.id
    })


@comm.route('/post/<int:comment_id>', methods=['GET'])
@login_required
def modify_post_comment(comment_id):
    comment = PostComment.query.filter_by(id=comment_id).first()
    if comment is None:
        return jsonify({
            'code': -1  # 指定 Comment 不存在
        })
    if current_user.modify_comment(comment, not comment.disabled):
        return jsonify({
            'code': 1  # 修改成功
        })
    return jsonify({
        'code': 0  # 修改失败
    })


@comm.route('/question/<int:comment_id>', methods=['GET'])
@login_required
def modify_question_comment(comment_id):
    comment = QuestionComment.query.filter_by(id=comment_id).first()
    if comment is None:
        return jsonify({
            'code': -1  # 指定 Comment 不存在
        })
    if current_user.modify_comment(comment, not comment.disabled):
        return jsonify({
            'code': 1  # 修改成功
        })
    return jsonify({
        'code': 0  # 修改失败
    })


@comm.route('/answer/<int:comment_id>', methods=['GET'])
@login_required
def modify_answer_comment(comment_id):
    comment = AnswerComment.query.filter_by(id=comment_id).first()
    if comment is None:
        return jsonify({
            'code': -1  # 指定 Comment 不存在
        })
    if current_user.modify_comment(comment, not comment.disabled):
        return jsonify({
            'code': 1  # 修改成功
        })
    return jsonify({
        'code': 0  # 修改失败
    })
