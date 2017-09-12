# -*- coding: utf-8 -*-
# @Time    : 2017/9/6 23:06
# @Author  : Forec
# @File    : post/views.py
# @Project : WildPointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn


from flask import render_template, redirect, flash, abort, url_for, request, current_app
from flask_login import login_required, current_user
from sqlalchemy import not_
from ..decorators import confirm_required

from . import post as pos
from .forms import PostEditForm
from .. import db
from ..models import Permission, Post, Tag


@pos.route('/', methods=['GET'])
def home():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.create.desc()).paginate(
        page, per_page=current_app.config['WP_POSTS_PER_PAGE'],
        error_out=False
    )
    posts = pagination.items
    hot_posts = Post.query.order_by(Post.score.asc()).slice(0, 6).all()
    hot_tags = Tag.query.order_by(Tag.count.asc()).slice(0, 16).all()
    return render_template('post/home.html', posts=posts, pagination=pagination, hot_posts=hot_posts,
                           tags=hot_tags, used_tags=[], type='post')


@pos.route('/me', methods=['GET'])
@login_required
@confirm_required
def me():
    query = current_user.posts
    page = request.args.get('page', 1, type=int)
    pagination = query.order_by(Post.last_edit.desc()).paginate(
        page, per_page=current_app.config['WP_POSTS_PER_PAGE'],
        error_out=False
    )
    posts = pagination.items
    post_count = int(len(posts) / 2) if len(posts) % 2 == 0 else int(len(posts) / 2) + 1
    posts_1 = posts[:post_count]
    posts_2 = posts[post_count:]
    return render_template('post/me.html', posts_1=posts_1, posts_2=posts_2, pagination=pagination)


@pos.route('/user/<int:user_id>', methods=['GET'])
def user(user_id):
    from ..models import User
    user = User.query.get_or_404(user_id)
    query = user.posts
    page = request.args.get('page', 1, type=int)
    pagination = query.order_by(Post.last_edit.desc()).paginate(
        page, per_page=current_app.config['WP_POSTS_PER_PAGE'],
        error_out=False
    )
    posts = pagination.items
    post_count = int(len(posts) / 2) if len(posts) % 2 == 0 else int(len(posts) / 2) + 1
    posts_1 = posts[:post_count]
    posts_2 = posts[post_count:]
    return render_template('post/user.html', user=user, posts_1=posts_1, posts_2=posts_2, pagination=pagination)


@pos.route('/follow', methods=['GET'])
@login_required
@confirm_required
def follow():
    query = current_user.followed_posts.filter(not_(Post.author_id == current_user.id))
    page = request.args.get('page', 1, type=int)
    pagination = query.order_by(Post.create.desc()).paginate(
        page, per_page=current_app.config['WP_POSTS_PER_PAGE'],
        error_out=False
    )
    posts = pagination.items
    hot_posts = Post.query.order_by(Post.score.asc()).slice(0, 6).all()
    hot_tags = Tag.query.order_by(Tag.count.asc()).slice(0, 16).all()
    return render_template('post/follow.html', posts=posts, pagination=pagination, hot_posts=hot_posts,
                           tags=hot_tags, used_tags=[], type='post')


@pos.route('/detail/<int:post_id>', methods=['GET'])
def detail(post_id):
    post = Post.query.get_or_404(post_id)
    moderate = False if not current_user.is_authenticated else \
        current_user.id == post.author_id or current_user.can(Permission.MODERATE_COMMENTS)
    has_liked = False if not current_user.is_authenticated else \
        current_user.confirmed and current_user.is_like_post(post)
    recent_posts = post.author.posts.order_by(Post.score.asc()).slice(0, 5).all()
    for i in range(0, len(recent_posts)):
        if recent_posts[i].id == post.id:
            recent_posts = recent_posts[:i] + recent_posts[i+1:]
            break
    tags = [item.tag for item in post.tags.all()]
    page = request.args.get('page', 1, type=int)
    pagination = post.comments.paginate(
        page, per_page=current_app.config['WP_COMMENTS_PER_PAGE'],
        error_out=False
    )
    comments = pagination.items
    return render_template('post/detail.html', post=post, tags=tags,
                           recent_posts=recent_posts, has_liked=has_liked,
                           moderate=moderate, pagination=pagination, comments=comments)
