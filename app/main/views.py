# -*- coding: utf-8 -*-
# @Time    : 2017/9/5 09:52
# @Author  : Forec
# @File    : main/views.py
# @Project : WildPointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn


from flask import render_template
from flask_login import current_user
from . import main
from ..models import Post, Question


@main.route('/', methods=['GET'])
def index():
    mail_address = 'None@None' if not current_user.is_authenticated else current_user.email
    mail_address = '#' if len(mail_address.split('#')) < 2 else mail_address.split('#')[1]
    mail_address = 'mail.' + mail_address
    posts = Post.query.order_by(Post.create.desc()).slice(0, 6)
    questions = Question.query.order_by(Question.create.desc()).slice(0, 6)
    return render_template('index.html', posts=posts, questions=questions, mail_address=mail_address)
