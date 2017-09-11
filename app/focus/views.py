# -*- coding: utf-8 -*-
# @Time    : 2017/9/10 23:51
# @Author  : Forec
# @File    : focus/views.py
# @Project : WildPointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn


from flask import request, current_app, render_template, abort
from flask_login import login_required, current_user
from . import focus
from ..models import User, Follow


@focus.route('/followers/<username>', methods=['GET'])
def followers(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        abort(404)
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.order_by(Follow.timestamp.desc()).paginate(
        page, per_page=current_app.config['WP_FOLLOWERS_PER_PAGE'], error_out=False)
    _followers = [item.follower for item in pagination.items]
    return render_template('focus/followers.html', pagination=pagination, followers=_followers, user=user)


@focus.route('/followed-by/<username>', methods=['GET'])
def followed_by(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        abort(404)
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.order_by(Follow.timestamp.desc()).paginate(
        page, per_page=current_app.config['WP_FOLLOWERS_PER_PAGE'], error_out=False)
    _followeds = [item.followed for item in pagination.items]
    return render_template('focus/followeds.html', pagination=pagination, followeds=_followeds, user=user)


@focus.route('/my-followers', methods=['GET'])
@login_required
def my_followers():
    page = request.args.get('page', 1, type=int)
    pagination = current_user.followers.order_by(Follow.timestamp.desc()).paginate(
        page, per_page=current_app.config['WP_FOLLOWERS_PER_PAGE'], error_out=False)
    _followers = [item.follower for item in pagination.items]
    return render_template('focus/my_followers.html', pagination=pagination, followers=_followers)


@focus.route('/my-following', methods=['GET'])
@login_required
def my_following():
    page = request.args.get('page', 1, type=int)
    pagination = current_user.followed.order_by(Follow.timestamp.desc()).paginate(
        page, per_page=current_app.config['WP_FOLLOWERS_PER_PAGE'], error_out=False)
    _followeds = [item.followed for item in pagination.items]
    return render_template('focus/my_followeds.html', pagination=pagination, followeds=_followeds)
