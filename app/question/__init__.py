# -*- coding: utf-8 -*-
# @Time    : 2017/9/5 15:40
# @Author  : Forec
# @File    : question/__init__.py
# @Project : WildPointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn


from flask import Blueprint

ques = Blueprint('ques', __name__)

from . import views, api

from ..models import Permission


@ques.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)