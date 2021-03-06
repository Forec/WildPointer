# -*- coding: utf-8 -*-
# @Time    : 2017/9/6 09:51
# @Author  : Forec
# @File    : models/post.py
# @Project : WildPointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn

from .relationship import LikePosts, PostTags
from .tag import Tag
from .. import db
from sqlalchemy import text
from datetime import datetime
from markdown import markdown
import bleach


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), index=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    type = db.Column(db.String(12), default="POST")
    has_image = db.Column(db.Boolean, default=False)
    score = db.Column(db.Integer, default=0)
    last_edit = db.Column(db.DateTime, default=datetime.utcnow)
    create = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    active = db.Column(db.Integer, default=0)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('PostComment', backref='post', lazy='dynamic')
    likers = db.relationship('LikePosts',
                             foreign_keys=[LikePosts.post_id],
                             backref=db.backref('post', lazy='joined'),
                             lazy='dynamic',
                             cascade='all, delete-orphan')
    tags = db.relationship('PostTags',
                           foreign_keys=[PostTags.post_id],
                           backref=db.backref('post', lazy='joined'),
                           lazy='dynamic',
                           cascade='all, delete-orphan')

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul', 'br',
                        'h1', 'h2', 'h3', 'p', 'img', 'href']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))
        target.has_image = target.body_html.find('<img') != -1

    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py
        seed()

        from .user import User

        user_count = User.query.count()
        for i in range(count):
            u = User.query.offset(randint(0, user_count-1)).first()
            p = Post(title=forgery_py.lorem_ipsum.words(randint(1, 2)),
                     body=forgery_py.lorem_ipsum.sentences(randint(1, 3)),
                     create=forgery_py.date.date(True),
                     author=u)
            db.session.add(p)
        db.session.commit()

    def has_tag(self, tag_name):
        tag = Tag.query.filter_by(name=tag_name).first()
        if tag is None:
            return False
        relation = PostTags.query.filter(text("post_id=:p and tag_id=:t")).params(p=self.id, t=tag.id).first()
        if relation:
            return True
        return False

    def remove_tag(self, tag_name):
        tag = Tag.query.filter_by(name=tag_name).first()
        if tag is None:
            return False
        relation = PostTags.query.filter(text("post_id=:p and tag_id=:t")).params(p=self.id, t=tag.id).first()
        if relation:
            db.session.delete(relation)
            tag.post_count = tag.post_count - 1
            tag.count = tag.count - 1
            db.session.add(tag)
            db.session.commit()
            return True
        return False

    def add_tag(self, tag_name):
        tag = Tag.query.filter_by(name=tag_name).first()
        if tag is None:
            tag = Tag(name=tag_name)
            db.session.add(tag)
            db.session.commit()
        relation = PostTags.query.filter(text("post_id=:p and tag_id=:t")).params(p=self.id, t=tag.id).first()
        if relation:
            return
        relation = PostTags(post_id=self.id, tag_id=tag.id)
        tag.post_count = tag.post_count + 1
        tag.count = tag.count + 1
        db.session.add(relation)
        db.session.add(tag)
        db.session.commit()

    def clear_tags(self):
        relations = PostTags.query.filter_by(post_id=self.id).all()
        for relation in relations:
            tag = Tag.query.filter_by(id=relation.tag_id).first()
            if tag:
                tag.post_count = tag.post_count - 1
                tag.count = tag.count - 1
                db.session.add(tag)
            db.session.delete(relation)
        db.session.commit()

    def fill_tag_by_names(self, tag_names):
        for tag_name in tag_names:
            tag = Tag.query.filter_by(name=tag_name).first()
            if tag is None:
                tag = Tag(name=tag_name)
                db.session.add(tag)
                db.session.commit()
            relation = PostTags(post_id=self.id, tag_id=tag.id)
            tag.post_count = tag.post_count + 1
            tag.count = tag.count + 1
            db.session.add(tag)
            db.session.add(relation)
        db.session.commit()

    def reset_tags(self, tag_names):
        self.clear_tags()
        self.fill_tag_by_names(tag_names)
