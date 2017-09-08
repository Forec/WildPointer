# -*- coding: utf-8 -*-
# @Time    : 2017/9/6 09:57
# @Author  : Forec
# @File    : models/comment.py
# @Project : WildPointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn


from .. import db
from datetime import datetime


class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    disabled = db.Column(db.Boolean, default=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comment_type = db.Column(db.String(16))

    __mapper_args__ = {
        'polymorphic_identity': 'Basic',
        'polymorphic_on': comment_type
    }


class PostComment(Comment):
    __tablename__ = "comment_posts"

    id = db.Column(db.Integer, db.ForeignKey('comments.id'), primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    __mapper_args__ = {
        'polymorphic_identity': 'post',

    }

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
            c = PostComment(body=forgery_py.lorem_ipsum.sentences(randint(1, 3)),
                            timestamp=forgery_py.date.date(True),
                            author=u,
                            disabled=False,
                            post=p)
            db.session.add(c)
        db.session.commit()

    @property
    def parent(self):
        return self.post


class QuestionComment(Comment):
    __tablename__ = "comment_questions"

    id = db.Column(db.Integer, db.ForeignKey('comments.id'), primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))

    __mapper_args__ = {
        'polymorphic_identity': 'question',
    }

    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py
        seed()

        from .user import User
        from .question import Question

        user_count = User.query.count()
        ques_count = Question.query.count()
        for i in range(count):
            u = User.query.offset(randint(0, user_count-1)).first()
            q = Question.query.offset(randint(0, ques_count-1)).first()
            c = QuestionComment(
                     body=forgery_py.lorem_ipsum.sentences(randint(1, 3)),
                     timestamp=forgery_py.date.date(True),
                     author=u,
                     disabled=False,
                     question=q)
            db.session.add(c)
        db.session.commit()

    @property
    def parent(self):
        return self.question


class AnswerComment(Comment):
    __tablename__ = "comment_answers"

    id = db.Column(db.Integer, db.ForeignKey('comments.id'), primary_key=True)
    answer_id = db.Column(db.Integer, db.ForeignKey('answers.id'))

    __mapper_args__ = {
        'polymorphic_identity': 'answer',
    }

    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py
        seed()

        from .user import User
        from .answer import Answer

        user_count = User.query.count()
        ans_count = Answer.query.count()
        for i in range(count):
            u = User.query.offset(randint(0, user_count-1)).first()
            a = Answer.query.offset(randint(0, ans_count-1)).first()
            c = AnswerComment(body=forgery_py.lorem_ipsum.sentences(randint(1, 3)),
                              timestamp=forgery_py.date.date(True),
                              author=u,
                              disabled=False,
                              answer=a)
            db.session.add(c)
        db.session.commit()

    @property
    def parent(self):
        return self.answer
