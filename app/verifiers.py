# -*- coding: utf-8 -*-
# @Time    : 2017/9/5 19:11
# @Author  : Forec
# @File    : verifiers.py
# @Project : WildPointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn

from .models import User
import re


def verify_email(email):
    if len(email) > 7 and re.match("^.+@(\[?)[a-zA-Z0-9\-\.]+\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) is not None:
        return True
    return False


def verify_username(username):
    if len(username) < 5 or len(username) > 16:
        return False
    invalid = ['?', '/', '=', '>', '<', '!', ',', ';', '.', '\\']
    for inv in invalid:
        if inv in username:
            return False
    return True


def verify_password(password):
    if len(password) < 8 or len(password) > 22:
        return False
    return True


def verify_token(email, token):
    if email is None or token is None or not verify_email(email):
        return None
    user = User.query.filter_by(email=email).first()
    if user is None:
        return None
    if user.verify_password_hash(token):
        return user
    return None
