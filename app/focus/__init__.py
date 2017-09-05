# -*- coding: utf-8 -*-
# @Time    : 2017/9/5 20:00
# @Author  : Forec
# @File    : focus/__init__.py
# @Project : WildPointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn


from flask import Blueprint

focus = Blueprint('focus', __name__)

from . import views

from ..models import Permission


@focus.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)