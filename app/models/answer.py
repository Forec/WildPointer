# -*- coding: utf-8 -*-
# @Time    : 2017/9/6 09:53
# @Author  : Forec
# @File    : models/answer.py
# @Project : WildPointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn


from .relationship import LikeAnswers, UnLikeAnswers
from .. import db
from datetime import datetime


class Answer(db.Model):
    __tablename__ = "answers"

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    score = db.Column(db.Integer, default=0, index=True)
    likers = db.relationship('LikeAnswers',
                             foreign_keys=[LikeAnswers.answer_id],
                             backref=db.backref('like_answers', lazy='joined'),
                             lazy='dynamic',
                             cascade='all, delete-orphan')
    unlikers = db.relationship('UnLikeAnswers',
                               foreign_keys=[UnLikeAnswers.answer_id],
                               backref=db.backref('unlike_answers', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')
    comments = db.relationship('AnswerComment', backref='answer', lazy='dynamic')

    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py
        seed()

        from .user import User
        from .question import Question

        user_count = User.query.count()
        question_count = Question.query.count()
        for i in range(count):
            u = User.query.offset(randint(0, user_count-1)).first()
            q = Question.query.offset(randint(0,  question_count-1)).first()
            t = Answer(body='```'+forgery_py.lorem_ipsum.sentences(randint(1, 3))+'```',
                       timestamp=forgery_py.date.date(True),
                       question=q,
                       author=u)
            db.session.add(t)
        db.session.commit()
