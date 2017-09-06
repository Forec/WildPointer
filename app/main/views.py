# -*- coding: utf-8 -*-
# @Time    : 2017/9/5 09:52
# @Author  : Forec
# @File    : main/views.py
# @Project : WildPointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn


from flask import render_template
from . import main
from ..models import Post, Question


@main.route('/', methods=['GET'])
def index():
    posts = Post.query.order_by(Post.timestamp.desc()).slice(0, 6)
    questions = Question.query.order_by(Question.timestamp.desc()).slice(0, 6)
    return render_template('index.html', posts=posts, questions=questions)
