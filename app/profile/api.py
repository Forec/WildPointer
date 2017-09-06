# -*- coding: utf-8 -*-
# @Time    : 2017/9/6 19:52
# @Author  : Forec
# @File    : profile/api.py
# @Project : WildPointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn


from flask import render_template, redirect, url_for, abort, flash, request, current_app, jsonify
from flask_login import login_required, current_user

from . import profile
from .forms import EditProfileForm, EditProfileAdminForm
from .. import db
from ..models import User, Role, Post, Answer
from ..decorators import admin_required


@profile.route('/summary/<username>', methods=['GET'])
def summary(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return jsonify({
            'code': -1   # 用户不存在
        })
    (posts, post_count) = (user.posts.order_by(Post.timestamp.desc())[:5], user.posts.count())
    (answers, answer_count) = (user.answers.order_by(Answer.timestamp.desc())[:5], user.answers.count())
    return jsonify({
        'code': 1,   # 查询成功
        'post_count': post_count,
        'answer_count': answer_count,
        'posts': [{'title': post.title, 'body': post.body_html} for post in posts],
        'answers': [{'title': answer.question.title, 'body': answer.body} for answer in answers],
        'username': username,
        'nickname': user.nickname,
        'id': user.id,
        'about_me': user.about_me,
        'location': user.location,
        'member_since': user.member_since,
        'last_seen': user.last_seen,
        'contact': user.contactE,
        'agree': user.agree
    })