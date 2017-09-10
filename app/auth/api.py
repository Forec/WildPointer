# -*- coding: utf-8 -*-
# @Time    : 2017/9/5 19:46
# @Author  : Forec
# @File    : auth/apis.py
# @Project : WildPointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn


from flask import request, jsonify, flash, redirect, url_for, render_template
from flask_login import login_required, login_user, current_user
from . import auth
from .. import db
from ..email import send_email
from ..verifiers import *
import json


@auth.route('/login', methods=['POST'])
def login():
    req = request.form.get('request')
    if req is None:
        return jsonify({
            'code': False
        })
    req = json.loads(req)
    username = req.get('username')
    password = req.get('password')
    if not password or not username or not verify_password(password):
        return jsonify({
            'code': False
        })
    if verify_email(username):
        user = User.query.filter_by(email=username).first()
    elif verify_username(username):
        user = User.query.filter_by(username=username).first()
    else:
        return jsonify({
            'code': False
        })
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
    flash("您已经成功注册了账户 " + user.username +
          "，我们已经向您注册时填写的邮箱发送了一封确认邮件，请您根据确认邮件的内容激活您的账户。")
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
            'code': 1,  # 已发送邮件修改邮箱
            'email': new_email
        })
    return jsonify({
        'code': 2  # 认证失败
    })


@auth.route('/forget', methods=['POST'])
def forget():
    req = request.form.get('request')
    if req is None:
        return jsonify({
            'code': 0  # 没有请求
        })
    if not current_user.is_anonymous:
        return jsonify({
            'code': 1  # 已经登陆
        })
    req = json.loads(req)
    email = req.get('email')
    if not verify_email(email):
        return jsonify({
            'code': 2  # 邮箱格式不正确
        })
    user = User.query.filter_by(email=email).first()
    if user:
        token = user.generate_reset_token()
        send_email(user.email, '重置您的密码', 'auth/email/reset_password', user=user, token=token,
                   next=request.args.get('next'))
    return jsonify({
        'code': 3  # 请求成功
    })


@auth.route('/reset/<token>', methods=['GET', 'POST'])
def reset(token):
    if not current_user.is_anonymous:
        flash('您已经登陆，如需修改密码，请在 "安全中心" 处理。')
        return redirect(url_for('auth.secure', _external=True))
    if request.method == 'GET':
        return render_template('auth/reset.html', token=token)
    else:
        req = request.form.get('request')
        if req is None:
            return jsonify({
                'code': 0  # 没有请求
            })
        req = json.loads(req)
        email = req.get('email')
        password = req.get('password')
        password2 = req.get('password2')
        if not verify_email(email) or not verify_password(password) or password != password2:
            return jsonify({
                'code': 2  # 邮箱／密码格式不正确
            })
        user = User.query.filter_by(email=email).first()
        if user is None:
            return jsonify({
                'code': 1  # 链接已失效
            })
        if user.reset_password(token, password):
            flash("您的密码已重置成功，请使用新密码登录。")
            return jsonify({
                'code': 3  # 重置成功
            })
        else:
            return jsonify({
                'code': 1  # 链接已失效
            })


@auth.route('/is_confirmed', methods=['GET'])
def is_confirmed():
    return jsonify({
        'code': current_user.is_authenticated and current_user.confirmed
    })
