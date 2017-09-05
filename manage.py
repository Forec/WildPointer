# -*- coding: utf-8 -*-
# @Time    : 2017/9/4 13:50
# @Author  : Forec
# @File    : manage.py
# @Software: Wild-Pointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn

from app import create_app, db
from app.models import User, Role, Post, Permission, Language, Task, Code, Comment, Advice
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app('dev')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
	return dict(app = app,
				db = db,
				User = User,
				Role = Role,
				Post = Post,
				Permission=Permission)

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
	'''Init the database'''
	db.drop_all()
	db.create_all()
	Role.insert_roles()
	Language.insert_languages()
	u = User(email='forec@bupt.edu.cn',\
			 username = 'forec',\
			 password = 'test',\
			 confirmed = True,\
			 role = Role.query.filter_by(name='Administrator').first(),\
			 location = 'Beijing, China',\
			 about_me = 'Wait for updating')
	u2 = User(email = 'test@test.com', \
			 username = 'test',\
			 password = 'test',\
			 role = Role.query.filter_by(name='User').first(),\
			 location = 'BUPT',\
			 about_me = 'test account',\
			 confirmed = True)
	db.session.add(u)
	db.session.add(u2)
	db.session.commit()
	User.generate_fake(10)
	Post.generate_fake(150)
	Task.generate_fake(150)
	Code.generate_fake(350)
	Comment.generate_fake(350)
	Advice.generate_fake(350)

if __name__ == "__main__":
	manager.run()