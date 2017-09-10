# -*- coding: utf-8 -*-
# @Time    : 2017/9/6 23:58
# @Author  : Forec
# @File    : post/api.py
# @Project : WildPointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn


from flask import jsonify, request, render_template, flash, abort
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
        if not body or len(body) > 100000:
            return jsonify({
                'code': 1  # 正文过长或没有正文
            })
        invalid_tag_char = '#,.!-=+/\\`~?$%^&*()@'
        for char in invalid_tag_char:
            if tags_string.find(char) != -1:
                return jsonify({
                    'code': 3  # 标签中包含不合法字符
                })
        tag_names = [tag_string.strip() for tag_string in tags_string.split(';')]
        if len(tag_names) > 5:
            return jsonify({
                'code': 2  # 标签数量过多
            })
        alphaB = 'abcdefghijklmnopqrstuvwxyz'
        for tag_name in tag_names:
            if len(tag_name) > 18:
                return jsonify({
                    'code': 3  # 标签长度过长
                })
            if len(tag_name) > 6:
                for char in tag_name:
                    if alphaB.find(char) == -1:
                        return jsonify({
                            'code': 3
                        })
        post = Post(author_id=current_user.id,
                    title=title,
                    body=body)
        db.session.add(post)
        db.session.commit()
        post.reset_tags(tag_names)
        db.session.add(post)
        db.session.commit()
        return jsonify({
            'code': 4,  # 成功
            'id': post.id
        })


@pos.route('/edit', methods=['POST'])
@pos.route('/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
@confirm_required
def edit(post_id=-1):
    post = Post.query.filter_by(id=post_id).first()
    if request.method == 'GET':
        if not post:
            abort(404)
        if post.author_id != current_user.id and not current_user.can(Permission.MODERATE_ALL):
            abort(403)
        tags = [item.tag for item in post.tags.all()]
        tags_string = ""
        for tag in tags:
            tags_string = tags_string + tag.name + ";"
        if len(tags) > 0:
            tags_string = tags_string[:-1]
        return render_template('post/edit.html', post=post, tags_string=tags_string)
    else:
        req = request.form.get('request')
        if req is None:
            return jsonify({
                'code': 0  # 没有请求
            })
        req = json.loads(req)
        if not post:
            post_id = -1 if not req.get('post_id') else req.get('post_id')
            post = Post.query.filter_by(id=post_id).first()
            if not post:
                return jsonify({
                    'code': -1  # 文章不存在
                })
        if post.author_id != current_user.id and not current_user.can(Permission.MODERATE_ALL):
            return jsonify({
                'code': -2  # 无权限
            })
        title = '无题' if not req.get('title') else req.get('title')
        body = req.get('body')
        tags_string = '' if not req.get('tags') else req.get('tags')
        if not body or len(body) > 100000:
            return jsonify({
                'code': 1  # 正文过长或没有正文
            })
        invalid_tag_char = '#,.!-=+/\\`~?$%^&*()@'
        for char in invalid_tag_char:
            if tags_string.find(char) != -1:
                return jsonify({
                    'code': 3  # 标签中包含不合法字符
                })
        tag_names = [tag_string.strip() for tag_string in tags_string.split(';')]
        if len(tag_names) > 5:
            return jsonify({
                'code': 2  # 标签数量过多
            })
        alphaB = 'abcdefghijklmnopqrstuvwxyz'
        for tag_name in tag_names:
            if len(tag_name) > 18:
                return jsonify({
                    'code': 3  # 标签长度过长
                })
            if len(tag_name) > 6:
                for char in tag_name:
                    if alphaB.find(char) == -1:
                        return jsonify({
                            'code': 3  # 标签长度过长
                        })
        post.title = title
        post.body = body
        db.session.add(post)
        db.session.commit()
        post.reset_tags(tag_names)
        db.session.add(post)
        db.session.commit()
        return jsonify({
            'code': 4,  # 成功
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
