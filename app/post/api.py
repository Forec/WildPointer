# -*- coding: utf-8 -*-
# @Time    : 2017/9/6 23:58
# @Author  : Forec
# @File    : post/api.py
# @Project : WildPointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn


from flask import jsonify
from flask_login import login_required, current_user

from . import post as pos
from ..models import Permission, Post
from ..decorators import confirm_required


@pos.route('/delete/<int:post_id>', methods=['GET'])
@login_required
def delete(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if not post:
        return jsonify({
            'code': -1  # 不存在对应 Post
        })
    if current_user.id != post.author_id and not current_user.can(Permission.MODERATE_ALL):
        return jsonify({
            'code': 0   # 无操作权限
        })
    if current_user.delete_post(post_id):
        return jsonify({
            'code': 1   # 删除成功
        })
    else:
        return jsonify({
            'code': 2   # 未知错误
        })


@pos.route('/like/<int:post_id>', methods=['GET'])
@login_required
@confirm_required
def like(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if not post:
        return jsonify({
            'code': -1  # 不存在对应 Post
        })
    if current_user.id == post.author_id:
        return jsonify({
            'code': 0   # 不能给自己点赞
        })

    post = current_user.like_post(post)
    if post:
        return jsonify({
            'code': 1,   # 点赞成功
            'count': post.score
        })
    else:
        return jsonify({
            'code': 2   # 未知错误
        })


@pos.route('/cancel_like/<int:post_id>', methods=['GET'])
@login_required
@confirm_required
def cancel_like(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if not post:
        return jsonify({
            'code': -1  # 不存在对应 Post
        })
    if current_user.id == post.author_id:
        return jsonify({
            'code': 0   # 不能给自己点赞／取消点赞
        })
    post = current_user.cancel_like_post(post)
    if post:
        return jsonify({
            'code': 1,   # 取消点赞成功
            'count': post.score
        })
    else:
        return jsonify({
            'code': 2   # 未知错误
        })
