# -*- coding: utf-8 -*-
# @Time    : 2017/9/6 15:39
# @Author  : Forec
# @File    : model/tag.py
# @Project : WildPointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn


from .relationship import PostTags, QuestionTags
from .. import db


class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), unique=True)
    post_count = db.Column(db.Integer, default=0)
    question_count = db.Column(db.Integer, default=0)
    posts = db.relationship('PostTags',
                            foreign_keys=[PostTags.tag_id],
                            backref=db.backref('tags', lazy='joined'),
                            lazy='dynamic',
                            cascade='all, delete-orphan')
    questions = db.relationship('QuestionTags',
                                foreign_keys=[QuestionTags.tag_id],
                                backref=db.backref('tags', lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan')