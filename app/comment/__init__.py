# -*- coding: utf-8 -*-
# @Time    : 2017/9/7 00:11
# @Author  : Forec
# @File    : comment/__init__.py
# @Project : WildPointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn


from flask import Blueprint

comment = Blueprint('comment', __name__)

from . import api

from ..models import Permission


@comment.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)