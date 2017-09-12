# -*- coding: utf-8 -*-
# @Time    : 2017/9/6 18:58
# @Author  : Forec
# @File    : answer/api.py
# @Project : WildPointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn


from flask import jsonify, request, flash
from flask_login import login_required, current_user
from . import ans
from .. import db
from ..models import Permission, Answer, Question, ContributeQuestions
from ..decorators import confirm_required
import json


#DEPRECATED
@ans.route('/detail/<int:answer_id>', methods=['GET'])
def detail(answer_id):
    answer = Answer.query.filter_by(id=answer_id).first()
    if answer is None:
        return jsonify({
            'code': -1  # 不存在对应 Answer
        })
    right = False
    if current_user.is_authenticated and current_user.id == answer.author_id:
        right = True
    return jsonify({
        'code': 0,
        'author_id': answer.author_id,
        'author_nickname': answer.author.nickname,
        'body': answer.body,
        'body_html': answer.body_html,
        'score': answer.score,
        'create': answer.create,
        'right': right
    })


@ans.route('/create', methods=['POST'])
@login_required
@confirm_required
def create():
    req = request.form.get('request')
    if req is None:
        return jsonify({
            'code': -1  # 无请求
        })
    req = json.loads(req)
    [body, question_id] = [req.get(name) for name in ['body', 'question_id']]
    if not body or not body.strip():
        return jsonify({
            'code': 2  # 答案不包括任何有效内容
        })
    if len(body) > 10000:
        return jsonify({
            'code': 3  # 答案过长
        })
    try:
        question_id = int(question_id)
    except ValueError:
        return jsonify({
            'code': 1  # 携带了违例信息
        })
    question = Question.query.filter_by(id=question_id).first()
    if not question:
        return jsonify({
            'code': -2   # 问题不存在
        })
    if current_user.is_contributor(question):
        return jsonify({
            'code': 0  # 已有回答
        })
    answer = Answer(question_id=question.id, author_id=current_user.id, body=body)
    relation = ContributeQuestions(question_id=question.id, contributor_id=current_user.id)
    db.session.add(relation)
    db.session.add(answer)
    db.session.commit()
    print("answer:", answer.create, " user:", current_user.last_seen)
    flash("您的答案已提交，您可以通过问题界面顶部的 \"查看我的回答\" 来查看您的答案。")
    return jsonify({
        'code': 4  # 创建成功
    })


#DEPRECATED
@ans.route('/modify', methods=['POST'])
@login_required
@confirm_required
def modify():
    req = request.form.get('request')
    if req is None:
        return jsonify({
            'code': -1  # 无请求
        })
    req = json.loads(req)
    [body, answer_id] = [req.get(name) for name in ['body', 'answer_id']]
    if not body or not body.strip():
        return jsonify({
            'code': 2  # 答案不包括任何有效内容
        })
    if len(body) > 10000:
        return jsonify({
            'code': 3  # 答案过长
        })
    try:
        answer_id = int(answer_id)
    except ValueError:
        return jsonify({
            'code': 1  # 携带了违例信息
        })
    answer = Answer.query.filter_by(id=answer_id).first()
    if not answer:
        return jsonify({
            'code': -2   # 答案不存在
        })
    if answer.author_id == current_user.id or current_user.can(Permission.MODERATE_ALL):
        answer.body = body
        db.session.add(answer)
        db.session.commit()
        return jsonify({
            'code': 4,  # 已有回答
            'body_html': answer.body_html
        })
    return jsonify({
        'code': 0  # 无权限
    })


#DEPRECATED
@ans.route('/delete', methods=['GET'])
@ans.route('/delete/<int:answer_id>', methods=['GET'])
@login_required
@confirm_required
def delete(answer_id=-1):
    answer = Answer.query.filter_by(id=answer_id).first()
    if not answer:
        return jsonify({
            'code': -1  # 不存在对应 Answer
        })
    if current_user.id != answer.author_id and not current_user.can(Permission.MODERATE_ALL):
        return jsonify({
            'code': 0   # 无操作权限
        })
    title = answer.question.title
    if current_user.delete_answer(answer_id):
        flash("您在问题《" + title + "》的回答已删除成功。")
        return jsonify({
            'code': 1   # 删除成功
        })
    else:
        return jsonify({
            'code': 2   # 未知错误
        })


@ans.route('/like/<int:answer_id>', methods=['GET'])
@login_required
@confirm_required
def like(answer_id):
    answer = Answer.query.filter_by(id=answer_id).first()
    if answer is None:
        return jsonify({
            'code': -1  # 对应 Answer 不存在
        })
    if current_user.id == answer.author_id:
        return jsonify({
            'code': 2  # 不能给自己点赞
        })
    if current_user.is_like_answer(answer):
        current_user.cancel_like_answer(answer)
        return jsonify({
            'code': 0,
            'score': answer.score
        })
    current_user.like_answer(answer)
    return jsonify({
        'code': 1,
        'score': answer.score
    })


@ans.route('/unlike/<int:answer_id>', methods=['GET'])
@login_required
@confirm_required
def unlike(answer_id):
    answer = Answer.query.filter_by(id=answer_id).first()
    if answer is None:
        return jsonify({
            'code': -1  # 对应 Question 不存在
        })
    if current_user.id == answer.author_id:
        return jsonify({
            'code': 2  # 不能反对自己的答案
        })
    if current_user.is_unlike_answer(answer):
        current_user.cancel_unlike_answer(answer)
        return jsonify({
            'code': 0,   # 已取消反对
            'score': answer.score
        })
    current_user.unlike_answer(answer)
    return jsonify({
        'code': 1,
        'score': answer.score
    })
