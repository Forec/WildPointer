# -*- coding: utf-8 -*-
# @Time    : 2017/9/6 23:06
# @Author  : Forec
# @File    : post/views.py
# @Project : WildPointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn


from flask import render_template, redirect, flash, abort, url_for, request, current_app, make_response
from flask_login import login_required, current_user
from ..decorators import confirm_required

from . import post as pos
from .forms import PostEditForm
from .. import db
from ..models import Permission, Post


@pos.route('/', methods=['GET'])
def home():
    show_followed = False
    if current_user.is_authenticated:
        show_followed = bool(request.cookies.get('show_followed', ''))
    if show_followed:
        query = current_user.followed_posts
    else:
        query = Post.query
    page = request.args.get('page', 1, type=int)
    pagination = query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['WP_POSTS_PER_PAGE'],
        error_out=False
    )
    posts = pagination.items
    return render_template('post/home.html', posts=posts, pagination=pagination, show_followed=show_followed)


@pos.route('/me', methods=['GET'])
@login_required
def me():
    query = Post.query.filter_by(author_id=current_user.id)
    page = request.args.get('page', 1, type=int)
    pagination = query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['WP_POSTS_PER_PAGE'],
        error_out=False
    )
    posts = pagination.items
    return render_template('post/me.html', posts=posts)


@pos.route('/show_all')
@login_required
def show_all():
    response = make_response(redirect(url_for('post.home')))
    response.set_cookie('show_followed', '', max_age=30*24*60*60)
    return response


@pos.route('/only_show_followed')
@login_required
def only_show_followed():
    response = make_response(redirect(url_for('post.home')))
    response.set_cookie('show_followed', '1', max_age=30*24*60*60)
    return response


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
    return render_template('post/detail.html', post=post, tags=post.tags.all(),
                           recent_posts=recent_posts, has_liked=has_liked,
                           moderate=moderate)


@pos.route('/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user != post.author and not current_user.can(Permission.MODERATE_ALL):
        abort(403)
    form = PostEditForm()
    if form.validate_on_submit():
        if not form.title.data:
            form.title.data = '无题'
        post.title = form.title.data
        post.body = form.body.data
        tags_string = form.tags.data
        tag_names = [tag_string.strip() for tag_string in tags_string.split(',')]
        post.reset_tags(tag_names)
        db.session.add(post)
        db.session.commit()
        flash('文章已更新')
        return redirect(url_for('post.detail', id=post.id))
    form.body.data = post.body
    form.title.data = post.title
    from functools import reduce
    form.tags.data = reduce(lambda x, y: x + ", " + y, [tag.name for tag in post.tags])
    return render_template('post/edit.html', form=form)


@pos.route('/create', methods=['GET', 'POST'])
@login_required
@confirm_required
def create():
    form = PostEditForm()
    if form.validate_on_submit():
        if not form.title.data:
            form.title.data = '无题'
        post = Post(title=form.title.data,
                    body=form.body.data)
        tags_string = form.tags.data
        tag_names = [tag_string.strip() for tag_string in tags_string.split(',')]
        post.reset_tags(tag_names)
        db.session.add(post)
        db.session.commit()
        flash('文章发布成功')
        return redirect(url_for('post.detail', id=post.id))
    return render_template('post/create.html', form=form)
