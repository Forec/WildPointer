# -*- coding: utf-8 -*-
# @Time    : 2017/9/5 19:46
# @Author  : Forec
# @File    : auth/apis.py
# @Project : WildPointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn


from flask import request, jsonify
from flask_login import login_required, login_user, current_user
from . import auth
from .. import db
from ..models import User
from ..email import send_email
from ..verifiers import verify_email, verify_username
import json


@auth.route('/login', methods=['POST'])
def login():
    req = request.form.get('request')
    if req is None:
        return jsonify({
            'code': False
        })
    req = json.loads(req)
    email = req.get('email')
    password = req.get('password')
    if email is None or password is None or not verify_email(email):
        return jsonify({
            'code': False
        })
    user = User.query.filter_by(email=email).first()
    if user is None or not user.verify_password(password):
        return jsonify({
            'code': False
        })
    else:
        login_user(user)
        return jsonify({
            'code': True
        })


@auth.route('/register', methods=['POST'])
def register():
    if current_user.is_authenticated:
        return jsonify({
            'code': -1   # 已经登陆，无需注册
        })
    req = request.form.get('request')
    if req is None:
        return jsonify({
            'code': 0  # 没有请求
        })
    req = json.loads(req)
    email = req.get('email')
    password = req.get('password')
    password2 = req.get('password2')
    username = req.get('username')
    if email is None or password is None or password2 is None or username is None or \
            not verify_email(email) or not verify_username(username) or password != password2:
        return jsonify({
            'code': 1  # 填写格式不对
        })
    user1 = User.query.filter_by(email=email).first()
    if user1 is not None:
        return jsonify({
            'code': 2  # 邮箱已被注册
        })

    user2 = User.query.filter_by(username=username).first()
    if user2 is not None:
        return jsonify({
            'code': 3  # 此用户名已被注册
        })
    user = User(email=email,
                username=username,
                nickname=username,
                password=password)
    db.session.add(user)
    db.session.commit()
    token = user.generate_confirmation_token()
    send_email(user.email,
               '确认您的帐户',
               'auth/email/confirm',
               user=user,
               token=token)
    login_user(user)
    return jsonify({
        'code': 4
    })


@auth.route('/resend_confirmation', methods=['GET'])
@login_required
def resend_confirmation():
    if current_user.confirmed:
        return jsonify({
            'code': 1   # 已经激活，无需重复激活
        })
    token = current_user.generate_confirmation_token()
    send_email(current_user.email,
               '确认您的帐户',
               'auth/email/confirm',
               user=current_user,
               token=token)
    return jsonify({
        'code': 0   # 已发送邮件，等待验证
    })


@auth.route('/change-password', methods=['POST'])
@login_required
def change_password():
    req = request.form.get('request')
    if req is None:
        return jsonify({
            'code': 0  # 没有请求
        })
    req = json.loads(req)
    old_password = req.get('old_password')
    new_password = req.get('new_password')
    if old_password == new_password:
        return jsonify({
            'code': 1  # 新／旧密码相同
        })
    if current_user.verify_password(old_password):
        current_user.password = new_password
        db.session.add(current_user)
        db.session.commit()
        return jsonify({
            'code': 2  # 修改成功
        })
    return jsonify({
        'code': 3  # 认证失败
    })


@auth.route('/change-email', methods=['POST'])
@login_required
def change_email_request():
    req = request.form.get('request')
    if req is None:
        return jsonify({
            'code': 0  # 没有请求
        })
    req = json.loads(req)
    password = req.get('password')
    new_email = req.get('email')
    if current_user.verify_password(password):
        token = current_user.generate_email_change_token(new_email)
        send_email(new_email, '确认您的邮箱', 'auth/email/change_email', user=current_user, token=token)
        return jsonify({
            'code': 1  # 已发送邮件修改邮箱
        })
    return jsonify({
        'code': 2  # 认证失败
    })
