# -*- coding: utf-8 -*-
# @Time    : 2017/9/4 13:50
# @Author  : Forec
# @File    : manage.py
# @Software: Wild-Pointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn


from app import create_app, db
from app.models import User, Role, Post, Answer, Question, PostComment, QuestionComment, AnswerComment, Tag
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app('production')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Post=Post, Answer=Answer, Question=Question)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)


@manager.command
def test():
    """Run the unit tests"""
    import unittest
    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def init():
    """Init databases"""
    db.drop_all()
    db.create_all()
    Role.insert_roles()
    u = User(email='forec@bupt.edu.cn',
             username='forec',
             nickname='Forec',
             password='password',
             confirmed=True,
             role=Role.query.filter_by(name='Administrator').first(),
             location='Beijing, China',
             about_me='Wait for updating')
    u2 = User(email='test@test.com',
              nickname='FlyingX',
              username='FlyingX',
              password='password',
              role=Role.query.filter_by(name='User').first(),
              location='Beijing University Of Posts and Telecommunications',
              about_me='Nong',
              confirmed=True)
    db.session.add(u)
    db.session.add(u2)
    db.session.commit()
#    User.generate_fake(10)
#    Post.generate_fake(150)
#    Question.generate_fake(350)
#    Tag.generate_fake(30, 100)
#    Answer.generate_fake(150)
#    PostComment.generate_fake(350)
#    QuestionComment.generate_fake(100)
#    AnswerComment.generate_fake(100)

if __name__ == "__main__":
    manager.run()
