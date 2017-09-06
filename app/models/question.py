# -*- coding: utf-8 -*-
# @Time    : 2017/9/6 09:54
# @Author  : Forec
# @File    : models/question.py
# @Project : WildPointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn


from .relationship import ContributeQuestions, LikeQuestions, UnLikeQuestions, QuestionTags
from .tag import Tag
from .. import db
from datetime import datetime


class Question(db.Model):
    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    score = db.Column(db.Integer, default=0)
    answer_count = db.Column(db.Integer, default=0)
    comment_count = db.Column(db.Integer, default=0)
    publisher_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    contributors = db.relationship('ContributeQuestions',
                                   foreign_keys=[ContributeQuestions.question_id],
                                   backref=db.backref('contributes', lazy='joined'),
                                   lazy='dynamic',
                                   cascade='all, delete-orphan')
    likers = db.relationship('LikeQuestions',
                             foreign_keys=[LikeQuestions.question_id],
                             backref=db.backref('like_questions', lazy='joined'),
                             lazy='dynamic',
                             cascade='all, delete-orphan')
    unlikers = db.relationship('UnLikeQuestions',
                               foreign_keys=[UnLikeQuestions.question_id],
                               backref=db.backref('unlike_questions', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')
    tags = db.relationship('QuestionTags',
                           foreign_keys=[QuestionTags.question_id],
                           backref=db.backref('tags', lazy='joined'),
                           lazy='dynamic',
                           cascade='all, delete-orphan')
    answers = db.relationship('Answer', backref='question', lazy='dynamic')
    comments = db.relationship('QuestionComment', backref='question', lazy='dynamic')

    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py
        seed()

        from .user import User

        user_count = User.query.count()
        for i in range(count):
            u = User.query.offset(randint(0, user_count-1)).first()
            q = Question(title=forgery_py.lorem_ipsum.words(randint(1, 2)),
                         body=forgery_py.lorem_ipsum.sentences(randint(1, 3)),
                         timestamp=forgery_py.date.date(True),
                         publisher=u)
            db.session.add(q)
            u.contribute(q)
        db.session.commit()

    def clear_tags(self):
        relations = QuestionTags.query.filter_by(question_id=self.id).all()
        for relation in relations:
            tag = relation.tag
            tag.question_count = tag.question_count - 1
            db.session.add(tag)
            db.session.delete(relation)

    def fill_tags(self, tags):
        for tag_name in tags:
            tag = Tag.query.filter_by(name=tag_name).first()
            if tag is None:
                tag = Tag(name=tag_name)
            relation = QuestionTags(question=self, tag=tag)
            tag.question_count = tag.question_count + 1
            db.session.add(tag)
            db.session.add(relation)

    def reset_tags(self, tags):
        self.clear_tags()
        self.fill_tags(tags)
