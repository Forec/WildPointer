# -*- coding: utf-8 -*-
# @Time    : 2017/9/6 18:58
# @Author  : Forec
# @File    : answer/api.py
# @Project : WildPointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn


from flask import jsonify
from flask_login import login_required, current_user
from . import ans
from ..models import Permission, Answer


@ans.route('/detail/<int:answer_id', methods=['GET'])
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
