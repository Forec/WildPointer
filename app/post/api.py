# -*- coding: utf-8 -*-
# @Time    : 2017/9/6 23:58
# @Author  : Forec
# @File    : post/api.py
# @Project : WildPointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn


from flask import jsonify, request, render_template, flash
from flask_login import login_required, current_user

from . import post as pos
from .. import db
from ..models import Permission, Post
from ..decorators import confirm_required
import json


@pos.route('/create', methods=['GET', 'POST'])
@login_required
@confirm_required
def create():
    if request.method == 'GET':
        return render_template('post/create.html')
    else:
        req = request.form.get('request')
        if req is None:
            return jsonify({
                'code': 0  # 没有请求
            })
        req = json.loads(req)
        title = '无题' if not req.get('title') else req.get('title')
        body = req.get('body')
        tags_string = '' if not req.get('tags') else req.get('tags')
        if not body or len(body) > 1400:
            return jsonify({
                'code': 1  # 正文过长或没有正文
            })
        invalid_tag_char = '#,.!-=+/\\`~?$%^&*()@'
        for char in invalid_tag_char:
            if tags_string.find(char) != -1:
                return jsonify({
                    'code': 2  # 标签中包含不合法字符
                })
        post = Post(author_id=current_user.id,
                    title=title,
                    body=body)
        db.session.add(post)
        db.session.commit()
        tag_names = [tag_string.strip() for tag_string in tags_string.split(';')]
        post.reset_tags(tag_names)
        db.session.add(post)
        db.session.commit()
        return jsonify({
            'code': 3,
            'id': post.id
        })


@pos.route('/delete/<int:post_id>', methods=['GET'])
@login_required
@confirm_required
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
    title = post.title
    if current_user.delete_post(post_id):
        flash("文章《" + title + "》" + "已删除。")
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
