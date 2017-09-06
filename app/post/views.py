# -*- coding: utf-8 -*-
# @Time    : 2017/9/6 23:06
# @Author  : Forec
# @File    : post/views.py
# @Project : WildPointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn


from flask import render_template, redirect, flash, abort, url_for, request, current_app, make_response
from flask_login import login_required, current_user

from . import post as pos
from .forms import PostEditForm
from .. import db
from ..models import Permission, Post, PostComment


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
    return render_template('index.html', posts=posts, pagination=pagination, show_followed=show_followed)


@pos.route('/show_all')
@login_required
def show_all():
    response = make_response(redirect(url_for('.index')))
    response.set_cookie('show_followed', '', max_age=30*24*60*60)
    return response


@pos.route('/only_show_followed')
@login_required
def only_show_followed():
    response = make_response(redirect(url_for('.index')))
    response.set_cookie('show_followed', '1', max_age=30*24*60*60)
    return response


@pos.route('/detail/<int:post_id>', methods=['GET'])
def detail(post_id):
    post = Post.query.get_or_404(post_id)
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) // current_app.config['WP_COMMENTS_PER_PAGE'] + 1
    pagination = post.comments.order_by(PostComment.timestamp.asc()).paginate(
        page, per_page=current_app.config['WP_COMMENTS_PER_PAGE'],
        error_out=False
    )
    comments = pagination.items
    return render_template('post/detail.html', comments=comments, pagination=pagination, post=post,
                           moderate=current_user.id == post.author_id or current_user.can(Permission.MODERATE_COMMENTS))


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
