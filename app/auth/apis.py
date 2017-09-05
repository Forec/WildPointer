# -*- coding: utf-8 -*-
# @Time    : 2017/9/5 19:46
# @Author  : Forec
# @File    : auth/apis.py
# @Project : WildPointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn


from flask import render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_user,  current_user

from . import auth
from .. import db
from ..models import User
from ..email import send_email
from ..verifiers import verify_email, verify_nickname
import json


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for('main.index', _external=True))
        return render_template('auth/login.html')
    else:
        req = request.form.get('request')
        if req is None:
            return 'fail'
        req = json.loads(req)
        email = req.get('email')
        password = req.get('passwd')
        if email is None or password is None or \
            not verify_email(email):
            return jsonify({
                'code': False
            })
        user = User.query.filter_by(email = email).first()
        if user is None or not user.verify_password(password):
            return jsonify({
                'code': False
            })
        else:
            login_user(user)
            return jsonify({
                'code': True
            })


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('您已经登录，无需注册！')
        return redirect(url_for('main.index', _external=True))
    if request.method == 'GET':
        return render_template('auth/register.html')
    else:
        req = request.form.get('request')
        if req is None:
            return jsonify({
                'code': 0   # 没有请求
            })
        req = json.loads(req)
        email = req.get('email')
        password = req.get('passwd')
        password2 = req.get('passwd2')
        nickname = req.get('nickname')
        if email is None or password is None or \
            password2 is None or nickname is None or \
            not verify_email(email) or not verify_nickname(nickname) or \
            password != password2:
            return jsonify({
                'code': 1   # 填写格式不对
            })
        user1 = User.query.filter_by(email = email).first()
        if user1 is not None:
            return jsonify({
                'code': 2      # 邮箱已被注册
            })

        user2 = User.query.filter_by(nickname = nickname).first()
        if user2 is not None:
            return jsonify({
                'code': 3      # 此昵称已被注册已被注册
            })
        user = User(email = email,
                    nickname = nickname,
                    password = password)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email,
                   '确认您的帐户',
                   'auth/email/confirm',
                   user=user,
                   token=token)
        flash('一封确认邮件已经发送到您填写的邮箱，'
              '请查看以激活您的帐号')
        login_user(user)
        return jsonify({
            'code': 4
        })