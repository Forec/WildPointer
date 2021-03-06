# -*- coding: utf-8 -*-
# @Time    : 2017/9/7 00:32
# @Author  : Forec
# @File    : message/api.py
# @Project : WildPointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn


from flask import render_template, redirect, url_for, abort, flash, request, current_app, make_response, jsonify
from flask_login import login_required, current_user
from . import message as mess
from .. import db
from ..models import Permission, Message


@mess.route('/tick', methods=['GET'])
@login_required
def tick():
    current_user.generate_messages()
    current_user.ping()
    messages = current_user.messages.filter_by(noticed=False).all()
    unread_count = current_user.messages.filter_by(viewed=False).count()
    message_bodys = []
    for message in messages:
        message_bodys.append(message.body)
        message.noticed = True
        db.session.add(message)
    db.session.commit()
    return jsonify({
        'code': 1,
        'count': len(messages),
        'messages': message_bodys,
        'receiver_id': current_user.id,
        'unread': unread_count
    })


@mess.route('/delete/<int:message_id>', methods=['GET'])
@login_required
def delete(message_id):
    message = Message.query.filter_by(id=message_id).first()
    if not message:
        return jsonify({
            'code': -1  # 不存在指定 message
        })
    if current_user != message.receiver and not current_user.can(Permission.ADMINISTER):
        return jsonify({
            'code': 0  # 认证失败
        })
    db.session.delete(message)
    return jsonify({
        'code': 1  # 删除成功
    })


@mess.route('/view/<int:message_id>', methods=['GET'])
@login_required
def view(message_id):
    message = Message.query.filter_by(id=message_id).first()
    if not message:
        return jsonify({
            'code': -1  # 不存在指定 message
        })
    if current_user != message.receiver and not current_user.can(Permission.ADMINISTER):
        return jsonify({
            'code': 0  # 认证失败
        })
    message.viewed = True
    db.session.add(message)
    return jsonify({
        'code': 1  # 修改状态成功
    })
