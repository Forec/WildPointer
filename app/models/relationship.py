# -*- coding: utf-8 -*-
# @Time    : 2017/9/6 09:54
# @Author  : Forec
# @File    : models/relationship.py
# @Project : WildPointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn


from .. import db
from datetime import datetime


class Follow(db.Model):
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    timestamp = db.Column(db.DateTime(), default=datetime.utcnow)


class LikePosts(db.Model):
    __tablename__ = 'likeposts'
    liker_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    timestamp = db.Column(db.DateTime(), default=datetime.utcnow)


class LikeQuestions(db.Model):
    __tablename__ = 'likequestions'
    liker_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), primary_key=True)
    timestamp = db.Column(db.DateTime(), default=datetime.utcnow)


class UnLikeQuestions(db.Model):
    __tablename__ = 'unlikequestions'
    unliker_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), primary_key=True)
    timestamp = db.Column(db.DateTime(), default=datetime.utcnow)


class LikeAnswers(db.Model):
    __tablename__ = 'likeanswers'
    liker_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    answer_id = db.Column(db.Integer, db.ForeignKey('answers.id'), primary_key=True)
    timestamp = db.Column(db.DateTime(), default=datetime.utcnow)


class UnLikeAnswers(db.Model):
    __tablename__ = 'unlikeanswers'
    unliker_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    answer_id = db.Column(db.Integer, db.ForeignKey('answers.id'), primary_key=True)
    timestamp = db.Column(db.DateTime(), default=datetime.utcnow)


class ContributeQuestions(db.Model):
    __tablename__ = 'contributes'
    contributor_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), primary_key=True)
    timestamp = db.Column(db.DateTime(), default=datetime.utcnow)


class PostTags(db.Model):
    __tablename__ = 'posttags'
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)


class QuestionTags(db.Model):
    __tablename__ = 'questiontags'
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)