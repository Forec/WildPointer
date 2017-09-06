# -*- coding: utf-8 -*-
# @Time    : 2017/9/6 18:58
# @Author  : Forec
# @File    : answer/__init__.py
# @Project : WildPointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn


from flask import Blueprint

ans = Blueprint('ans', __name__)

from . import views, api

from ..models import Permission


@ans.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)