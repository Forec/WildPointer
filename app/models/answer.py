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
from markdown import markdown
import bleach


class Answer(db.Model):
    __tablename__ = "answers"

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    type = db.Column(db.String(12), default="ANSWER")
    create = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    last_edit = db.Column(db.DateTime, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    score = db.Column(db.Integer, default=0, index=True)
    active = db.Column(db.Integer, default=0)  # whether there are new activities
    likers = db.relationship('LikeAnswers',
                             foreign_keys=[LikeAnswers.answer_id],
                             backref=db.backref('answer', lazy='joined'),
                             lazy='dynamic',
                             cascade='all, delete-orphan')
    unlikers = db.relationship('UnLikeAnswers',
                               foreign_keys=[UnLikeAnswers.answer_id],
                               backref=db.backref('answer', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')
    comments = db.relationship('AnswerComment', backref='answer', lazy='dynamic')

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul', 'br',
                        'h1', 'h2', 'h3', 'p', 'img', 'href']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

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
            t = Answer(body='> '+forgery_py.lorem_ipsum.sentences(randint(1, 3)),
                       create=forgery_py.date.date(True),
                       question=q,
                       author=u)
            db.session.add(t)
        db.session.commit()
