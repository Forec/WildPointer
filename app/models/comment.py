# -*- coding: utf-8 -*-
# @Time    : 2017/9/6 09:57
# @Author  : Forec
# @File    : models/comment.py
# @Project : WildPointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn


from .. import db
from datetime import datetime
from markdown import markdown
import bleach


class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    disabled = db.Column(db.Boolean, default=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'code', 'em', 'i', 'br', 'strong']
        target.body_html = bleach.linkify(
            bleach.clean(markdown(value, output_format='html'),
                         tags=allowed_tags, strip=True)
        )


class PostComment(Comment):
    __tablename__ = "post_comments"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py
        seed()

        from .user import User
        from .post import Post

        user_count = User.query.count()
        post_count = Post.query.count()
        for i in range(count):
            u = User.query.offset(randint(0, user_count-1)).first()
            p = Post.query.offset(randint(0, post_count-1)).first()
            c = Comment(
                     body=forgery_py.lorem_ipsum.sentences(randint(1, 3)),
                     timestamp=forgery_py.date.date(True),
                     author=u,
                     disabled=False,
                     post=p)
            db.session.add(c)
        db.session.commit()


class QuestionComment(Comment):
    __tablename__ = "question_comments"

    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))

    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py
        seed()

        from .user import User
        from .post import Post

        user_count = User.query.count()
        post_count = Post.query.count()
        for i in range(count):
            u = User.query.offset(randint(0, user_count-1)).first()
            p = Post.query.offset(randint(0, post_count-1)).first()
            c = Comment(
                     body=forgery_py.lorem_ipsum.sentences(randint(1, 3)),
                     timestamp=forgery_py.date.date(True),
                     author=u,
                     disabled=False,
                     post=p)
            db.session.add(c)
        db.session.commit()


class AnswerComment(Comment):

    __tablename__ = "answer_comments"

    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id'))

    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py
        seed()

        from .user import User
        from .post import Post

        user_count = User.query.count()
        post_count = Post.query.count()
        for i in range(count):
            u = User.query.offset(randint(0, user_count-1)).first()
            p = Post.query.offset(randint(0, post_count-1)).first()
            c = Comment(
                     body=forgery_py.lorem_ipsum.sentences(randint(1, 3)),
                     timestamp=forgery_py.date.date(True),
                     author=u,
                     disabled=False,
                     post=p)
            db.session.add(c)
        db.session.commit()
