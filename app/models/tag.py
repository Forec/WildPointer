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
    name = db.Column(db.String(16), unique=True, index=True, default='untitled')
    post_count = db.Column(db.Integer, default=0)
    question_count = db.Column(db.Integer, default=0)
    count = db.Column(db.Integer, default=0)
    posts = db.relationship('PostTags',
                            foreign_keys=[PostTags.tag_id],
                            backref=db.backref('tag', lazy='joined'),
                            lazy='dynamic',
                            cascade='all, delete-orphan')
    questions = db.relationship('QuestionTags',
                                foreign_keys=[QuestionTags.tag_id],
                                backref=db.backref('tag', lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan')

    def get_posts(self):
        from .post import Post
        return Post.query.join(PostTags, PostTags.post_id == Post.id).filter(PostTags.tag_id == self.id)

    def get_questions(self):
        from .question import Question
        return Question.query.join(QuestionTags, QuestionTags.question_id == Question.id).\
            filter(QuestionTags.tag_id == self.id)

    @staticmethod
    def generate_fake(tag_count=30, relation_count=100):
        from random import seed, randint
        import forgery_py
        seed()

        from ..models import Post, Question
        from sqlalchemy.exc import IntegrityError

        post_count = Post.query.count()
        question_count = Question.query.count()

        for i in range(tag_count):
            tag = Tag(name=forgery_py.lorem_ipsum.word()[:12])
            db.session.add(tag)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

        tag_count = Tag.query.count()

        for i in range(int(relation_count/2)):
            tag = Tag.query.offset(randint(0, tag_count-1)).first()
            p = Post.query.offset(randint(0, post_count-1)).first()
            relation = PostTags.query.filter_by(post_id=p.id).filter_by(tag_id=tag.id).first()
            if relation:
                continue
            relation = PostTags(post_id=p.id, tag_id=tag.id)
            db.session.add(relation)

        for i in range(int(relation_count/2)):
            tag = Tag.query.offset(randint(0, tag_count-1)).first()
            q = Question.query.offset(randint(0, question_count-1)).first()
            relation = QuestionTags.query.filter_by(question_id=q.id).filter_by(tag_id=tag.id).first()
            if relation:
                continue
            relation = QuestionTags(question_id=q.id, tag_id=tag.id)
            db.session.add(relation)

        db.session.commit()
