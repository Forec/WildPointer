# -*- coding: utf-8 -*-
# @Time    : 2017/9/6 23:06
# @Author  : Forec
# @File    : post/__init__.py
# @Project : WildPointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn


from flask import Blueprint

post = Blueprint('post', __name__)

from . import views, api

from ..models import Permission


@post.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)