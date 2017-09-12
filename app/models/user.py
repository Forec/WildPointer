# -*- coding: utf-8 -*-
# @Time    : 2017/9/6 09:48
# @Author  : Forec
# @File    : models/user.py
# @Project : WildPointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn

from .permission import Permission
from .role import Role
from .relationship import *
from .. import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer
from flask import current_app, request
from datetime import datetime
import hashlib


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    contactE = db.Column(db.String(64))
    confirmed = db.Column(db.Boolean, default=False)
    disabled = db.Column(db.Boolean, default=False)
    password_hash = db.Column(db.String(128))
    avatar_hash = db.Column(db.String(32))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    website = db.Column(db.String(512), default='')
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    username = db.Column(db.String(64), unique=True, index=True)
    nickname = db.Column(db.String(64), index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    agree = db.Column(db.Integer, default=0, index=True)

    from .message import Message
    messages = db.relationship('Message', backref='receiver', lazy='dynamic', foreign_keys=[Message.receiver_id])
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    post_comments = db.relationship('PostComment', backref='author', lazy='dynamic')
    questions = db.relationship('Question', backref='publisher', lazy='dynamic')
    question_comments = db.relationship('QuestionComment', backref='author', lazy='dynamic')
    answers = db.relationship('Answer', backref='author', lazy='dynamic')
    answer_comments = db.relationship('AnswerComment', backref='author', lazy='dynamic')
    followed = db.relationship('Follow',
                               foreign_keys=(Follow.follower_id,),
                               backref=db.backref('follower', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')
    followers = db.relationship('Follow',
                                foreign_keys=(Follow.followed_id,),
                                backref=db.backref('followed', lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan')
    contributes = db.relationship('ContributeQuestions',
                                  foreign_keys=[ContributeQuestions.contributor_id],
                                  backref=db.backref('contributor', lazy='joined'),
                                  lazy='dynamic',
                                  cascade='all, delete-orphan')
    like_posts = db.relationship('LikePosts',
                                 foreign_keys=[LikePosts.liker_id],
                                 backref=db.backref('liker', lazy='joined'),
                                 lazy='dynamic',
                                 cascade='all, delete-orphan')
    like_questions = db.relationship('LikeQuestions',
                                     foreign_keys=[LikeQuestions.liker_id],
                                     backref=db.backref('liker', lazy='joined'),
                                     lazy='dynamic',
                                     cascade='all, delete-orphan')
    unlike_questions = db.relationship('UnLikeQuestions',
                                       foreign_keys=[UnLikeQuestions.unliker_id],
                                       backref=db.backref('unliker', lazy='joined'),
                                       lazy='dynamic',
                                       cascade='all, delete-orphan')
    like_answers = db.relationship('LikeAnswers',
                                   foreign_keys=[LikeAnswers.liker_id],
                                   backref=db.backref('liker', lazy='joined'),
                                   lazy='dynamic',
                                   cascade='all, delete-orphan')
    unlike_answers = db.relationship('UnLikeAnswers',
                                     foreign_keys=[UnLikeAnswers.unliker_id],
                                     backref=db.backref('unliker', lazy='joined'),
                                     lazy='dynamic',
                                     cascade='all, delete-orphan')

    @property
    def password(self):
        raise AttributeError('密码为非可读项！')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return password is not None and check_password_hash(self.password_hash, password)

    def verify_password_hash(self, password_hash):
        return self.password_hash == password_hash

    def generate_confirmation_token(self, expiration=3600):
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def generate_email_change_token(self, new_email, expiration=3600):
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.id, 'new_email': new_email})

    def generate_reset_token(self, expiration=3600):
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def reset_password(self, token, new_password):
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        db.session.commit()
        return True

    def confirm(self, token):
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        if self.role is None:
            self.role = Role.query.filter_by(name='普通用户').first()
        elif self.role.name == '未激活用户':
            self.role = Role.query.filter_by(name='普通用户').first()
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True

    def is_confirmed(self):
        return self.confirmed

    def change_email(self, token):
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None or self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        self.avatar_hash = hashlib.md5(new_email.encode('utf-8')).hexdigest()
        db.session.add(self)
        db.session.commit()
        return True

    def delete_post(self, post_id):
        from .post import Post
        post = Post.query.filter_by(id=post_id).first()
        if post is None or (post.author_id != self.id and not self.can(Permission.MODERATE_ALL)):
            return False
        db.session.delete(post)
        return True

    # admin_required
    def delete_question(self, question_id):
        from .question import Question
        question = Question.query.filter_by(id=question_id).first()
        if question is None or (not self.can(Permission.MODERATE_ALL)):
            return False
        db.session.delete(question)
        return True

    def delete_message(self, token):
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('delete') is None or data.get('user') is None:
            return False
        message_id = data.get('delete')
        from .message import Message
        message = Message.query.filter_by(id=message_id).first()
        user = User.query.filter_by(id=data.get('user')).first()
        if message is None:
            return False
        if user.id != self.id and user.id != message.sender_id:
            return False
        db.session.delete(message)
        db.session.commit()
        return True

    def gravatar(self, size=100, default='identicon', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash_link = self.avatar_hash or hashlib.md5(self.email.encode('utf-8')).hexdigest()
        return "{url}/{hash_link}?s={size}&d={default}&r={rating}".format(
            url=url, hash_link=hash_link, size=size, default=default, rating=rating
        )

    def can(self, permissions):
        return self.role is not None and (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    # Part about Comments
    def modify_comment(self, comment, disable):
        if comment is None:
            return False
        from ..models import PostComment, AnswerComment, QuestionComment
        if comment.author_id == self.id or self.can(Permission.MODERATE_COMMENTS) or \
                (isinstance(comment, PostComment) and comment.post.author_id == self.id) or \
                (isinstance(comment, QuestionComment) and comment.question.publisher_id == self.id) or \
                (isinstance(comment, AnswerComment) and comment.answer.author_id == self.id):
            comment.disable = disable
            db.session.add(comment)
            return True
        return False

    # Like part about Posts
    def like_post(self, post):
        if not self.is_like_post(post):
            relation = LikePosts(liker_id=self.id, post_id=post.id)
            author = post.author
            post.score = post.score + 1
            author.agree = author.agree + 1
            db.session.add(relation)
            db.session.add(author)
            db.session.add(post)
            return post
        return None

    def cancel_like_post(self, post):
        relation = self.like_posts.filter_by(post_id=post.id).first()
        if relation:
            author = post.author
            author.agree = author.agree - 1
            post.score = post.score - 1
            db.session.delete(relation)
            db.session.add(author)
            db.session.add(post)
            return post
        return None

    def is_like_post(self, post):
        return self.like_posts.filter_by(post_id=post.id).first() is not None

    # Like part about Questions, like/unlike questions won't affect the publisher
    def like_question(self, question):
        if self.is_unlike_question(question):
            self.cancel_unlike_question(question)
        if not self.is_like_question(question):
            relation = LikeQuestions(liker_id=self.id, question_id=question.id)
            question.score = question.score + 1
            db.session.add(relation)
            db.session.add(question)

    def cancel_like_question(self, question):
        relation = self.like_questions.filter_by(question_id=question.id).first()
        if relation:
            question.score = question.score - 1
            db.session.delete(relation)
            db.session.add(question)

    def unlike_question(self, question):
        if self.is_like_question(question):
            self.cancel_like_question(question)
        if not self.is_unlike_question(question):
            relation = UnLikeQuestions(unliker_id=self.id, question_id=question.id)
            question.score = question.score - 1
            db.session.add(relation)
            db.session.add(question)

    def cancel_unlike_question(self, question):
        relation = self.unlike_questions.filter_by(question_id=question.id).first()
        if relation:
            question.score = question.score + 1
            db.session.delete(relation)
            db.session.add(question)

    def is_like_question(self, question):
        return self.like_questions.filter_by(question_id=question.id).first() is not None

    def is_unlike_question(self, question):
        return self.unlike_questions.filter_by(question_id=question.id).first() is not None

    # Like part about Answers, only likes will affect on the author of answer
    def like_answer(self, answer):
        if self.is_unlike_answer(answer):
            self.cancel_unlike_answer(answer)
        if not self.is_like_answer(answer):
            relation = LikeAnswers(liker_id=self.id, answer_id=answer.id)
            author = answer.author
            answer.score = answer.score + 1
            author.agree = author.agree + 1
            db.session.add(relation)
            db.session.add(author)
            db.session.add(answer)

    def cancel_like_answer(self, answer):
        relation = self.like_answers.filter_by(answer_id=answer.id).first()
        if relation:
            author = answer.author
            answer.score = answer.score - 1
            author.agree = author.agree - 1
            db.session.delete(relation)
            db.session.add(author)
            db.session.add(answer)

    def unlike_answer(self, answer):
        if self.is_like_answer(answer):
            self.cancel_like_answer(answer)
        if not self.is_unlike_answer(answer):
            relation = UnLikeAnswers(unliker_id=self.id, answer_id=answer.id)
            answer.score = answer.score - 1
            db.session.add(relation)
            db.session.add(answer)

    def cancel_unlike_answer(self, answer):
        relation = self.unlike_answers.filter_by(answer_id=answer.id).first()
        if relation:
            answer.score = answer.score + 1
            db.session.delete(relation)
            db.session.add(answer)

    def is_like_answer(self, answer):
        return self.like_answers.filter_by(answer_id=answer.id).first() is not None

    def is_unlike_answer(self, answer):
        return self.unlike_answers.filter_by(answer_id=answer.id).first() is not None

    # User relationship part, follow/un-follow users
    def follow(self, user):
        if not self.is_following(user):
            relation = Follow(follower=self, followed=user)
            db.session.add(relation)

    def unfollow(self, user):
        relation = self.followed.filter_by(followed_id=user.id).first()
        if relation:
            db.session.delete(relation)

    def is_following(self, user):
        return self.followed.filter_by(followed_id=user.id).first() is not None

    def is_followed_by(self, user):
        return self.followers.filter_by(follower_id=user.id).first() is not None

    @property
    def followed_posts(self):
        from .post import Post
        return Post.query.join(Follow, Follow.followed_id == Post.author_id).\
            filter(Follow.follower_id == self.id)

    # Questions contribute
    def contribute(self, question):
        if not self.is_contributor(question):
            relation = ContributeQuestions(contributor_id=self.id, question_id=question.id)
            db.session.add(relation)

    def uncontribute(self, question):
        relation = question.contributors.filter_by(contributor_id=self.id).first()
        if relation:
            db.session.delete(relation)
            return True
        return False

    def is_contributor(self, question):
        if not question:
            return False
        return question.contributors.filter_by(contributor_id=self.id).first() is not None

    def get_answer_id(self, question):
        answer = question.answers.filter_by(author_id=self.id).first()
        if answer:
            return answer.id
        return -1

    def add_answer(self, question, answer_body):
        if question is None or not answer_body:
            return None
        from .answer import Answer
        answer = Answer(body=answer_body,
                        author=self,
                        question=question)
        db.session.add(answer)
        self.contribute(question)

    def delete_answer(self, answer_id):
        from .answer import Answer
        answer = Answer.query.filter_by(id=answer_id).first()
        if answer is None or (answer.author_id != self.id and not self.can(Permission.MODERATE_ALL)):
            return False
        self.uncontribute(answer.question)
        db.session.delete(answer)
        return True

    # messages part
    def generate_messages(self):
        from .post import Post
        from .question import Question
        from .answer import Answer
        from flask import url_for

        message_list = []

        # 未读的关注文章
        unread_followed_posts = self.followed_posts.filter(Post.create > self.last_seen).all()
        if unread_followed_posts:
            new_message = "您关注的用户" + unread_followed_posts[0].author.nickname
            for post in unread_followed_posts[1:3]:
                new_message += "、" + post.author.nickname
            if len(unread_followed_posts) > 3:
                new_message += "等 " + str(len(unread_followed_posts)) + " 人"
            new_message += "新发布了文章<a href=\"" + \
                           url_for('post.detail', post_id=unread_followed_posts[0].id, _external=True) + \
                           "\">《" + unread_followed_posts[0].title + "》</a>"
            for post in unread_followed_posts[1:]:
                new_message += "、<a href=\"" + url_for('post.detail', post_id=post.id, _external=True) + \
                               "\">《" + post.title + "》</a>"
            new_message += "。"
            message_list.append(new_message)

        # 有新动态的问题及其对应的回答数量
        active_questions = []
        active_answers_count = 0
        for question in self.questions:
            print(question.title)
            #TODO
            for answer in question.answers:
                print(answer.create, self.last_seen, answer.create > self.last_seen)
            question_answer_active_count = question.answers.filter(Answer.create > self.last_seen).count()
            # print(question.title, question_answer_active_count)
            if question_answer_active_count > 0:
                active_questions.append(question)
                active_answers_count += question_answer_active_count
        if active_questions:
            new_message = "您提出的<a href=\"" + \
                          url_for('ques.detail', question_id=active_questions[0].id, _external=True) + \
                          "\">《" + active_questions[0].title + "》</a>"
            for question in active_questions[1:3]:
                new_message += "、<a href=\"" + \
                               url_for('ques.detail', question_id=question.id, _external=True) + \
                               "\">《" + question.title + "》</a>"
            if len(active_questions) > 3:
                new_message += "等 " + str(len(active_questions)) + " 个问题新产生了共 "
            else:
                new_message += "新产生了共 "
            new_message += str(active_answers_count) + " 个回答。"
            message_list.append(new_message)

        # 将消息存入数据库
        from .message import Message
        for message in message_list:
            # print(message)
            mdb = Message(body=message, receiver_id=self.id)
            db.session.add(mdb)
        db.session.commit()


    @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py
        seed()
        for i in range(count):
            u = User(email=forgery_py.internet.email_address(),
                     nickname=forgery_py.internet.user_name(True),
                     username=forgery_py.internet.user_name(True),
                     contactE=forgery_py.internet.email_address(),
                     password=forgery_py.lorem_ipsum.word(),
                     confirmed=True,
                     location=forgery_py.address.city(),
                     about_me=forgery_py.lorem_ipsum.sentence(),
                     member_since=forgery_py.date.date(True))
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['EMAIL_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = hashlib.md5(
                self.email.encode('utf-8')
            ).hexdigest()
        # self.follow(self)

    @staticmethod
    def add_self_follows():
        for user in User.query.all():
            if not user.is_following(user):
                user.follow(user)
                db.session.add(user)
                db.session.commit()

    def __repr__(self):
        return '<User %r>' % self.nickname
