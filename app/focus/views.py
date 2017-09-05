# -*- coding: utf-8 -*-
# @Time    : 2017/9/5 19:55
# @Author  : Forec
# @File    : focus/views.py
# @Project : WildPointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn

from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user

from . import focus
from ..models import User, Permission
from ..decorators import permission_required


@focus.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('不合法的用户')
        return redirect(url_for('.index'))
    if current_user.is_following(user):
        flash('您已关注该用户')
        return redirect(url_for('.user', username=username))
    current_user.follow(user)
    flash('您已关注用户 %s' % user.username)
    return redirect(url_for('.user', username=username))


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


@focus.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('不合法的用户')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(
        page, per_page=current_app.config['WP_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.follower, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('main/followers.html', user=user, title="的关注者",
                           endpoint='.followers', pagination=pagination,
                           follows=follows)


@focus.route('/followed-by/<username>')
def followed_by(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('不合法的用户')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(
        page, per_page=current_app.config['WP_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.followed, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('main/followers.html', user=user, title="关注的人",
                           endpoint='.followed_by', pagination=pagination,
                           follows=follows)