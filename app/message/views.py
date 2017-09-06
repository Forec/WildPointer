# -*- coding: utf-8 -*-
# @Time    : 2017/9/7 00:32
# @Author  : Forec
# @File    : message/views.py
# @Project : WildPointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn


from flask import render_template, request, current_app
from flask_login import login_required, current_user

from . import message as mess
from ..models import Message


@mess.route('/')
@login_required
def message():
    unread_messages = current_user.messages.order_by(Message.viewed.asc()).order_by(Message.timestamp.desc())
    page = request.args.get('page', 1, type=int)
    pagination = unread_messages.paginate(
        page, per_page=current_app.config['WP_MESSAGES_PER_PAGE'],
        error_out=False
    )
    latest_messages = pagination.items
    return render_template('message/home.html', messages=latest_messages, pagination=pagination)


@mess.route('/detail/<int:message_id>')
@login_required
def detail(message_id):
    message = Message.query.get_or_404(message_id)
    return render_template('message/detail.html', message=message)