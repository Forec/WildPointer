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
from sqlalchemy import text
from datetime import datetime
from markdown import markdown
import bleach


class Question(db.Model):
    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    create = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    last_edit = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    score = db.Column(db.Integer, default=0)
    active = db.Column(db.Integer, default=0)
    answer_count = db.Column(db.Integer, default=0)
    comment_count = db.Column(db.Integer, default=0)
    publisher_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    contributors = db.relationship('ContributeQuestions',
                                   foreign_keys=[ContributeQuestions.question_id],
                                   backref=db.backref('question', lazy='joined'),
                                   lazy='dynamic',
                                   cascade='all, delete-orphan')
    likers = db.relationship('LikeQuestions',
                             foreign_keys=[LikeQuestions.question_id],
                             backref=db.backref('question', lazy='joined'),
                             lazy='dynamic',
                             cascade='all, delete-orphan')
    unlikers = db.relationship('UnLikeQuestions',
                               foreign_keys=[UnLikeQuestions.question_id],
                               backref=db.backref('question', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')
    tags = db.relationship('QuestionTags',
                           foreign_keys=[QuestionTags.question_id],
                           backref=db.backref('question', lazy='joined'),
                           lazy='dynamic',
                           cascade='all, delete-orphan')
    answers = db.relationship('Answer', backref='question', lazy='dynamic')
    comments = db.relationship('QuestionComment', backref='question', lazy='dynamic')

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

        user_count = User.query.count()
        for i in range(count):
            u = User.query.offset(randint(0, user_count-1)).first()
            q = Question(title=forgery_py.lorem_ipsum.words(randint(1, 2)),
                         body=forgery_py.lorem_ipsum.sentences(randint(1, 3)),
                         create=forgery_py.date.date(True),
                         publisher=u)
            db.session.add(q)
        db.session.commit()

    def has_tag(self, tag_name):
        tag = Tag.query.filter_by(name=tag_name).first()
        if tag is None:
            return False
        relation = QuestionTags.query.filter(text("question_id=:q and tag_id=:t")).params(q=self.id, t=tag.id).first()
        if relation:
            return True
        return False

    def remove_tag(self, tag_name):
        tag = Tag.query.filter_by(name=tag_name).first()
        if tag is None:
            return False
        relation = QuestionTags.query.filter(text("question_id=:q and tag_id=:t")).params(q=self.id, t=tag.id).first()
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
        relation = QuestionTags.query.filter(text("question_id=:q and tag_id=:t")).params(q=self.id, t=tag.id).first()
        if relation:
            return
        relation = QuestionTags(post_id=self.id, tag_id=tag.id)
        tag.post_count = tag.post_count + 1
        tag.count = tag.count + 1
        db.session.add(relation)
        db.session.add(tag)
        db.session.commit()

    def clear_tags(self):
        relations = QuestionTags.query.filter_by(question_id=self.id).all()
        for relation in relations:
            tag = relation.tag
            tag.question_count = tag.question_count - 1
            tag.count = tag.count - 1
            db.session.add(tag)
            db.session.delete(relation)

    def fill_tag_by_names(self, tags):
        for tag_name in tags:
            tag = Tag.query.filter_by(name=tag_name).first()
            if tag is None:
                tag = Tag(name=tag_name)
                db.session.add(tag)
                db.session.commit()
            relation = QuestionTags(question_id=self.id, tag_id=tag.id)
            tag.question_count = tag.question_count + 1
            tag.count = tag.count + 1
            db.session.add(tag)
            db.session.add(relation)
        db.session.commit()

    def reset_tags(self, tags):
        self.clear_tags()
        self.fill_tags(tags)
