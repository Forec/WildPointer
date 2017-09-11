# -*- coding: utf-8 -*-
# @Time    : 2017/9/6 19:52
# @Author  : Forec
# @File    : profile/api.py
# @Project : WildPointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn


from flask import jsonify, url_for, request
from flask_login import current_user, login_required
from flask_moment import _moment
from . import profile
from .. import db
from ..models import User, Permission
import json


@profile.route('/', methods=['GET'])
@profile.route('/summary/<username>', methods=['GET'])
def summary(username=''):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return jsonify({
            'code': -1   # 用户不存在
        })
    post_count = user.posts.count()
    answer_count = user.answers.count()
    question_count = user.questions.count()
    isself = True if current_user.is_authenticated and current_user.id == user.id else False
    admin = True if current_user.can(Permission.ADMINISTER) else False
    return jsonify({
        'code': 1,   # 查询成功
        'post_count': post_count,
        'answer_count': answer_count,
        'question_count': question_count,
        'username': username,
        'nickname': user.nickname,
        'admin': admin,
        'id': user.id,
        'self': isself,
        'about_me': user.about_me,
        'location': user.location,
        'create': _moment(user.member_since).format('LLL'),
        'last_seen': _moment(user.last_seen).format('LLL'),
        'email': user.contactE,
        'agree': user.agree,
        'img': user.gravatar(size=48),
        'posts_url': url_for('post.user', user_id=user.id, _external=True) if not isself else url_for('post.me', _external=True),
        'questions_url': url_for('ques.user', user_id=user.id, _external=True) if not isself else url_for('ques.me', _external=True),
        'answers_url': url_for('ans.user', user_id=user.id, _external=True) if not isself else url_for('ans.me', _external=True),
        'followers_url': url_for('focus.followers', username=user.username, _external=True) if not isself else url_for('focus.my_followers', _extrnal=True),
        'followeds_url': url_for('focus.followed_by', username=user.username, _external=True) if not isself else url_for('focus.my_following', _external=True),
        'follower_count': user.followers.count(),
        'followed_count': user.followed.count(),
        'disabled': user.disabled,
        'is_login': current_user.is_authenticated,
        'is_following': current_user.is_authenticated and current_user.is_following(user)
    })


@profile.route('/edit', methods=['POST'])
@login_required
def edit():
    req = request.form.get('request')
    if req is None:
        return jsonify({
            'code': 0  # 没有请求
        })
    req = json.loads(req)
    username = req.get('username')
    if not username:
        return jsonify({
            'code': 1  # 无法识别用户
        })
    disabled = req.get('disabled')
    if disabled is not None and disabled != 'pass' and not current_user.can(Permission.ADMINISTER):
        return jsonify({
            'code': 2  # 无权限
        })
    disabled = False if not disabled else disabled
    user = User.query.filter_by(username=username).first()
    if not user or (user.id != current_user.id and not current_user.can(Permission.ADMINISTER)):
        return jsonify({
            'code': 2  # 无权限
        })
    user.nickname = '' if not req.get('nickname') else req.get('nickname')
    user.location = '' if not req.get('address') else req.get('address')
    user.contactE = '' if not req.get('email') else req.get('email')
    user.website = '' if not req.get('homepage') else req.get('homepage')
    user.about_me = '' if not req.get('about_me') else req.get('about_me')
    if disabled != 'pass':
        if isinstance(disabled, bool):
            user.disabled = disabled
    db.session.add(user)
    db.session.commit()
    return jsonify({
        'code': 3  # 成功
    })
