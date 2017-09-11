# -*- coding: utf-8 -*-
# @Time    : 2017/9/5 00:21
# @Author  : Forec
# @File    : decorators.py
# @Software: Wild-Pointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn


from functools import wraps
from flask import abort
from flask_login import current_user
from .models import Permission


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def confirm_required(p):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or not current_user.confirmed or current_user.disabled:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator(p)


def admin_required(f):
    return permission_required(Permission.ADMINISTER)(f)
