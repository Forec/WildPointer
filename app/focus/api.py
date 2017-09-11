# -*- coding: utf-8 -*-
# @Time    : 2017/9/6 22:38
# @Author  : Forec
# @File    : focus/api.py
# @Project : WildPointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn


from flask import redirect, url_for, flash, jsonify
from flask_login import login_required, current_user

from . import focus
from ..models import User, Permission
from ..decorators import permission_required


@focus.route('/follow/<username>', methods=['GET'])
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return jsonify({
            'code': -1  # 不存在目标用户
        })
    if user.id == current_user.id:
        return jsonify({
            'code': 0  # 不能关注自己
        })
    if current_user.is_following(user):
        return jsonify({
            'code': 1,  # 已关注此用户
            'nickname': user.nickname
        })
    current_user.follow(user)
    return jsonify({
        'code': 2,  # 关注成功
        'nickname': user.nickname
    })


@focus.route('/unfollow/<username>', methods=['GET'])
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return jsonify({
            'code': -1  # 不存在目标用户
        })
    if user.id == current_user.id:
        return jsonify({
            'code': 0  # 不能关注／取关自己
        })
    if not current_user.is_following(user):
        return jsonify({
            'code': 1,  # 并未关注此用户
            'nickname': user.nickname
        })
    current_user.unfollow(user)
    return jsonify({
        'code': 2,  # 取消关注成功
        'nickname': user.nickname
    })
