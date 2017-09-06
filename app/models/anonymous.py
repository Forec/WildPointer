# -*- coding: utf-8 -*-
# @Time    : 2017/9/6 10:12
# @Author  : Forec
# @File    : models/anonymous.py
# @Project : WildPointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn


from .user import User
from .. import login_manager
from flask_login import AnonymousUserMixin


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
