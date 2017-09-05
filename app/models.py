# -*- coding: utf-8 -*-
# @Time    : 2017/9/4 22:47
# @Author  : Forec
# @File    : models.py
# @Software: Wild-Pointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn


from . import db
from . import login_manager
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer
from flask import current_app, request
from datetime import datetime
from markdown import markdown
import hashlib
import bleach

class Permission:
    FOLLOW = 0x01  # follow other users
    COMMENT = 0x02  # comment on other users' articles
    WRITE_ARTICLES = 0x04  # write articles
    MODERATE_COMMENTS = 0x08  # moderate users' comments
    MODERATE_TASKS = 0x10
    ADMINISTER = 0x80  # administer

class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime,index= True, default=datetime.utcnow)
    disabled = db.Column(db.Boolean, default = False)
    author_id= db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'code', 'em', 'i','br',
                        'strong']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py
        seed()
        user_count = User.query.count()
        post_count = Post.query.count()
        for i in range(count):
            u = User.query.offset(randint(0, user_count-1)).first()
            p = Post.query.offset(randint(0, post_count-1)).first()
            c = Comment(
                     body = forgery_py.lorem_ipsum.sentences(randint(1,3)),
                     timestamp=forgery_py.date.date(True),
                     author = u,
                     disabled = False,
                     post = p)
            db.session.add(c)
        db.session.commit()

class Advice(db.Model):
    __tablename__ = 'advices'

    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime,index= True, default=datetime.utcnow)
    accept = db.Column(db.Boolean, default = False)
    close = db.Column(db.Boolean, default = False)
    viewed = db.Column(db.Boolean, default= False)
    author_id= db.Column(db.Integer, db.ForeignKey('users.id'))
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))
    target_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # author = db.relationship('User', foreign_keys =[author_id] )
    # target = db.relationship('User', foreign_keys = [target_id])
    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'code', 'em', 'i', 'br',
                        'strong']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))
    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py
        seed()
        user_count = User.query.count()
        task_count = Task.query.count()
        for i in range(count):
            u = User.query.offset(randint(0, user_count-1)).first()
            t = Task.query.offset(randint(0, task_count-1)).first()
            a = Advice(
                     body = forgery_py.lorem_ipsum.sentences(randint(1,3)),
                     timestamp=forgery_py.date.date(True),
                     author = u,
                     accept = False,
                     close = False,
                     viewed = False,
                    target = t.publisher,
                     task = t)
            db.session.add(a)
        db.session.commit()

class LikeCodes(db.Model):
    __tablename__ = 'likecodes'

    liker_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                         primary_key = True)
    code_id = db.Column(db.Integer, db.ForeignKey('codes.id'),
                        primary_key = True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class ViewProblems(db.Model):
    __tablename__ = 'viewproblems'

    viewer_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                          primary_key = True)
    problem_id = db.Column(db.Integer, db.ForeignKey('tasks.id'),
                           primary_key= True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class SolveProblems(db.Model):
    __talbename__ = 'solves'

    solver_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                          primary_key =True)
    problem_id = db.Column(db.Integer, db.ForeignKey('tasks.id'),
                           primary_key = True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class ContributeProblems(db.Model):
    __talbename__ = 'contributes'

    contributer_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                          primary_key =True)
    problem_id = db.Column(db.Integer, db.ForeignKey('tasks.id'),
                           primary_key = True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index= True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    confirmed = db.Column(db.Boolean, default=False)
    score = db.Column(db.Integer, default = 2)
    publisher_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    contributors = db.relationship('ContributeProblems',
                                   foreign_keys=[ContributeProblems.problem_id],
                                   backref=db.backref('contributes', lazy='joined'),
                                   lazy = 'dynamic',
                                   cascade = 'all, delete-orphan')
    solvers = db.relationship('SolveProblems',
                             foreign_keys=[SolveProblems.problem_id],
                             backref = db.backref('solves', lazy='joined'),
                             lazy = 'dynamic',
                             cascade='all, delete-orphan')
    viewers = db.relationship('ViewProblems',
                              foreign_keys=[ViewProblems.problem_id],
                              backref=db.backref('views', lazy='joined'),
                              lazy = 'dynamic',
                              cascade = 'all, delete-orphan')
    codes = db.relationship('Code', backref='task', lazy = 'dynamic')
    advices = db.relationship('Advice', backref='task', lazy = 'dynamic')

    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py
        seed()
        user_count = User.query.count()
        for i in range(count):
            u = User.query.offset(randint(0, user_count-1)).first()
            t = Task(title=forgery_py.lorem_ipsum.words(randint(1,2)),
                     confirmed = True,
                     body = forgery_py.lorem_ipsum.sentences(randint(1,3)),
                     timestamp=forgery_py.date.date(True),
                     publisher =u)
            db.session.add(t)
            u.contribute(t)
        db.session.commit()

class Code(db.Model):
    __tablename__ = "codes"

    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.Text)
    language_id = db.Column(db.Integer, db.ForeignKey('languages.id'))
    timestamp = db.Column(db.DateTime, index = True, default = datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))
    passed = db.Column(db.Boolean, default=False)
    likes = db.Column(db.Integer, default= 0, index= True)
    likers = db.relationship('LikeCodes',
                                   foreign_keys=[LikeCodes.code_id],
                                   backref=db.backref('likes', lazy='joined'),
                                   lazy = 'dynamic',
                                   cascade = 'all, delete-orphan')
    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py
        seed()
        user_count = User.query.count()
        language_count = Language.query.count()
        task_count = Task.query.count()
        for i in range(count):
            u = User.query.offset(randint(0, user_count-1)).first()
            l = Language.query.offset(randint(0, language_count-1)).first()
            blT = Task.query.offset(randint(0,  task_count-1)).first()
            t = Code(body = '```'+forgery_py.lorem_ipsum.sentences(randint(1,3))+'```',
                     timestamp=forgery_py.date.date(True),
                     passed = bool(randint(0,1)),
                     author =u,
                     language = l,
                     task = blT,
                     likes = randint(1,40)
                     )
            db.session.add(t)
        db.session.commit()

class Follow(db.Model):
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                            primary_key = True)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                             primary_key = True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    default = db.Column(db.Boolean, default=False)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'Uncheck_user': (0x00, True),
            'User': (Permission.FOLLOW |
                     Permission.COMMENT |
                     Permission.WRITE_ARTICLES, False),
            'Moderator_comments': (Permission.FOLLOW |
                          Permission.COMMENT |
                          Permission.WRITE_ARTICLES |
                          Permission.MODERATE_COMMENTS, False),
            'Moderator_tasks':(
                Permission.COMMENT |
                Permission.WRITE_ARTICLES |
                Permission.MODERATE_TASKS, False
            ),
            'Administrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    contactE = db.Column(db.String(64))
    confirmed = db.Column(db.Boolean, default=False)
    password_hash = db.Column(db.String(128))
    avatar_hash = db.Column(db.String(32))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default = datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default = datetime.utcnow)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    score = db.Column(db.Integer, default=20, index=True)
    agree = db.Column(db.Integer, default = 0, index=True)

    messages = db.relationship('Advice', backref='target', lazy='dynamic',
                               foreign_keys = [Advice.target_id])
    posts = db.relationship('Post', backref='author', lazy = 'dynamic')
    publishs = db.relationship('Task', backref='publisher', lazy='dynamic')
    advices = db.relationship('Advice', backref='author', lazy='dynamic',
                              foreign_keys = [Advice.author_id])
    followed = db.relationship('Follow',
                               foreign_keys= [Follow.follower_id],
                               backref = db.backref('follower', lazy='joined'),
                               lazy = 'dynamic',
                               cascade='all, delete-orphan')
    followers = db.relationship('Follow',
                               foreign_keys= [Follow.followed_id],
                               backref = db.backref('followed', lazy='joined'),
                               lazy = 'dynamic',
                               cascade='all, delete-orphan')
    solves = db.relationship('SolveProblems',
                             foreign_keys=[SolveProblems.solver_id],
                             backref=db.backref('solver',lazy='joined'),
                             lazy = 'dynamic',
                             cascade='all, delete-orphan')
    contributes = db.relationship('ContributeProblems',
                                  foreign_keys=[ContributeProblems.contributer_id],
                                  backref=db.backref('contributor', lazy='joined'),
                                  lazy = 'dynamic',
                                  cascade='all, delete-orphan')
    views = db.relationship('ViewProblems',
                              foreign_keys=[ViewProblems.viewer_id],
                              backref=db.backref('viewer', lazy='joined'),
                              lazy = 'dynamic',
                              cascade = 'all, delete-orphan')
    likes = db.relationship('LikeCodes',
                              foreign_keys=[LikeCodes.liker_id],
                              backref=db.backref('liker', lazy='joined'),
                              lazy = 'dynamic',
                              cascade = 'all, delete-orphan')
    comments = db.relationship('Comment',backref='author', lazy='dynamic')
    codes = db.relationship('Code', backref='author', lazy = 'dynamic')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash= generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    def generate_confirmation_token(self, expiration=3600):
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm':self.id})
    def generate_email_change_token(self, new_email, expiration = 3600):
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.id, 'new_email': new_email})
    def generate_reset_token(self, expiration=3600):
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})
    def generate_delete_token(self, postid, expiration):
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'delete': postid, 'user':self.id})

    def reset_password(self, token ,new_password):
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
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY']) # match logged user
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        if self.role == None:
            self.role = Role.query.filter_by(name = 'User').first()
        elif self.role.name == 'Uncheck_user':
            self.role = Role.query.filter_by(name='User').first()
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True

    def change_email(self, token):
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email = new_email).first() is not None:
            return False
        self.email = new_email
        self.avatar_hash = hashlib.md5(new_email.encode('utf-8')).hexdigest()
        db.session.add(self)
        db.session.commit()
        return True

    def delete_post(self, token):
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('delete') is None:
            return False
        if data.get('user') is None:
            return False
        user = User.query.filter_by(id=data.get('user')).first()
        if user.id != self.id  and \
            not user.can(Permission.ADMINISTER):
            return False
        postid = data.get('delete')
        post =Post.query.filter_by(id=postid).first()
        if post is None or (post.author_id != self.id and not user.can(Permission.ADMINISTER)):
            return False
        db.session.delete(post)
        db.session.commit()
        return True

    def delete_task(self, token):
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('delete') is None:
            return False
        if data.get('user') is None:
            return False
        user = User.query.filter_by(id=data.get('user')).first()
        if user.id != self.id  and \
            not user.can(Permission.ADMINISTER):
            return False
        taskid = data.get('delete')
        task =Task.query.filter_by(id=taskid).first()
        if task is None or (task.publisher_id != self.id and not user.can(Permission.ADMINISTER)):
            return False
        db.session.delete(task)
        db.session.commit()
        return True

    def delete_code(self, token):
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return -1
        if data.get('delete') is None:
            return -1
        if data.get('user') is None:
            return -1
        user = User.query.filter_by(id=data.get('user')).first()
        if not user.can(Permission.ADMINISTER):
            return -1
        codeid = data.get('delete')
        code =Code.query.filter_by(id=codeid).first()
        taskid = code.task_id
        if code is None or (not user.can(Permission.ADMINISTER)):
            return -1
        db.session.delete(code)
        db.session.commit()
        return taskid

    def delete_advice(self, token):
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return -1
        if data.get('delete') is None:
            return -1
        if data.get('user') is None:
            return -1
        adviceid = data.get('delete')
        advice =Advice.query.filter_by(id=adviceid).first()
        user = User.query.filter_by(id=data.get('user')).first()
        if not user.can(Permission.ADMINISTER) and not user == advice.author:
            return -1
        taskid = advice.task_id
        if advice is None:
            return -1
        db.session.delete(advice)
        db.session.commit()
        return taskid

    def gravatar(self, size=100, default='identicon', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url= 'http://www.gravatar.com/avatar'
        hash = self.avatar_hash or \
               hashlib.md5(self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url = url, hash = hash, size=size, default = default, rating = rating
        )

    def can(self, permissions):
        return self.role is not None and \
               (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def like(self, code):
        if not self.is_like(code):
            l = LikeCodes(liker = self, likes = code)
            author = code.author
            author.agree = author.agree + 1
            code.likes = code.likes + 1
            db.session.add(l)
            db.session.add(author)
            db.session.add(code)

    def unlike(self,code):
        l = self.likes.filter_by(code_id=code.id).first()
        if l:
            author = code.author
            author.agree = author.agree - 1
            code.likes = code.likes - 1
            db.session.delete(l)
            db.session.add(author)
            db.session.add(code)

    def is_like(self,code):
        return self.likes.filter_by(
            code_id = code.id
        ).first() is not None

    def follow(self, user):
        if not self.is_following(user):
            f = Follow(follower=self, followed=user)
            db.session.add(f)

    def unfollow(self, user):
        f = self.followed.filter_by(followed_id=user.id).first()
        if f:
            db.session.delete(f)

    def is_following(self, user):
        return self.followed.filter_by(
            followed_id = user.id
        ).first() is not None

    def is_followed_by(self, user):
        return self.followers.filter_by(
            follower_id = user.id
        ).first() is not None

    def solve(self,task):
        if not self.is_contributer(task):
            s = SolveProblems(solver=self, solves = task)
            db.session.add(s)
            db.session.commit()

    def is_solver(self,task):
        return task.solvers.filter_by(
            solver_id = self.id
        ).first() is not None

    def contribute(self, task):
        if not self.is_contributor(task):
            c = ContributeProblems(contributor=self, contributes =task)
            db.session.add(c)
            db.session.commit()

    def is_contributor(self, task):
        return task.contributors.filter_by(
                contributer_id = self.id
        ).first() is not None

    def view(self, task):
        if not self.is_viewer(task):
            v = ViewProblems(viewer = self, views = task)
            db.session.add(v)
            db.session.commit()

    def is_viewer(self, task):
        return task.viewers.filter_by(
                viewer_id = self.id
        ).first() is not None

    def is_spaner(self, task):
        return self.publishs.filter_by(
            id = task.id
        ).first() is not None

    def is_submitter(self, task):
        return self.codes.filter_by(
            task = task
        ).first() is not None

    @property
    def followed_posts(self):
        return Post.query.join(Follow, Follow.followed_id==Post.author_id).\
            filter(Follow.follower_id==self.id)

    @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py
        seed()
        for i in range(count):
            u = User(email=forgery_py.internet.email_address(),
                     username = forgery_py.internet.user_name(True),
                     contactE = forgery_py.internet.email_address(),
                     password = forgery_py.lorem_ipsum.word(),
                     confirmed = True,
                     location = forgery_py.address.city(),
                     about_me = forgery_py.lorem_ipsum.sentence(),
                     member_since = forgery_py.date.date(True))
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['EMAIL_ADMIN']:
                self.role = Role.query.filter_by(permission=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = hashlib.md5(
                self.email.encode('utf-8')
            ).hexdigest()
        self.follow(self)

    @staticmethod
    def add_self_follows():
        for user in User.query.all():
            if not user.is_following(user):
                user.follow(user)
                db.session.add(user)
                db.session.commit()

    def __repr__(self):
        return '<User %r>' % self.username

class Post(db.Model):

    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(128), index= True)
    disabled = db.Column(db.Boolean, default=False)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index = True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comment',backref='post', lazy='dynamic')

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul', 'br',
                        'h1', 'h2', 'h3', 'p']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))


    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py
        seed()
        user_count = User.query.count()
        for i in range(count):
            u = User.query.offset(randint(0, user_count-1)).first()
            p = Post(title=forgery_py.lorem_ipsum.words(randint(1,2)),
                     disabled= False,
                    body = forgery_py.lorem_ipsum.sentences(randint(1,3)),
                     timestamp=forgery_py.date.date(True),
                     author = u)
            db.session.add(p)
        db.session.commit()

class Language(db.Model):
    __tablename__ = 'languages'

    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(64), unique=True, index=True)
    codes = db.relationship('Code', backref= 'language', lazy = 'dynamic')

    @staticmethod
    def insert_languages():
        languages = ["C", "C++", "Python", "Java", "Haskell", "Golang", "JavaScript", "Scala", "Scheme"]
        for l in languages:
            lan = Language.query.filter_by(language=l).first()
            if lan is None:
                language = Language(language=l)
            db.session.add(language)
        db.session.commit()

    def __repr__(self):
        return '<Language %r>' % self.language


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False
    def is_administrator(self):
        return False

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

login_manager.anonymous_user = AnonymousUser

db.event.listen(Post.body, 'set', Post.on_changed_body)
db.event.listen(Comment.body, 'set', Comment.on_changed_body)
