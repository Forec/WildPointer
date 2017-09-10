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
def home():
    unread_messages = current_user.messages.order_by(Message.viewed.asc()).order_by(Message.timestamp.desc())
    page = request.args.get('page', 1, type=int)
    pagination = unread_messages.paginate(
        page, per_page=current_app.config['WP_MESSAGES_PER_PAGE'],
        error_out=False
    )
    messages = pagination.items
    message_count = int(len(messages) / 2) if len(messages) % 2 == 0 else int(len(messages) / 2) + 1
    messages_1 = messages[:message_count]
    messages_2 = messages[message_count:]
    return render_template('message/list.html', messages_1=messages_1, messages_2=messages_2, pagination=pagination)
