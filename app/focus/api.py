# -*- coding: utf-8 -*-
# @Time    : 2017/9/6 22:38
# @Author  : Forec
# @File    : focus/api.py
# @Project : WildPointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn


from flask import redirect, url_for, flash, request, current_app, jsonify
from flask_login import login_required, current_user

from . import focus
from ..models import User, Permission, Follow
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
    if current_user.is_following(user):
        return jsonify({
            'code': 1  # 已关注此用户
        })
    current_user.follow(user)
    return jsonify({
        'code': 2  # 关注成功
    })


@focus.route('/unfollow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('不合法的用户')
        return redirect(url_for('.index'))
    if not current_user.is_following(user):
        flash('您并未关注该用户')
        return redirect(url_for('.user', username=username))
    current_user.unfollow(user)
    flash('您已取消对用户 %s 的关注' % user.username)
    return redirect(url_for('.user', username=username))


@focus.route('/followers/<username>', methods=['GET'])
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return jsonify({
            'code': -1
        })
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.order_by(Follow.timestamp.desc()).paginate(
        page, per_page=current_app.config['WP_FOLLOWERS_PER_PAGE'], error_out=False)
    user_followers = [item.follower for item in pagination.items]
    user_followers_dict = [{'username': u.username,
                            'icon_url': u.gravatar(size=48),
                            'link': url_for('profile.detail', username=u.username),
                            'about_me': u.about_me} for u in user_followers]
    return jsonify({
        'code': 1,  # 获取成功
        'followers': user_followers_dict
    })


@focus.route('/followed-by/<username>', methods=['GET'])
def followed_by(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return jsonify({
            'code': -1
        })
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.order_by(Follow.timestamp.desc()).paginate(
        page, per_page=current_app.config['WP_FOLLOWERS_PER_PAGE'], error_out=False)
    user_followeds = [item.followed for item in pagination.items]
    user_followeds_dict = [{'username': u.username,
                            'icon_url': u.gravatar(size=48),
                            'link': url_for('profile.detail', username=u.username),
                            'about_me': u.about_me} for u in user_followeds]
    return jsonify({
        'code': 1,  # 获取成功
        'followers': user_followeds_dict
    })
