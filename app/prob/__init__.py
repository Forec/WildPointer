# -*- coding: utf-8 -*-
# @Time    : 2017/9/5 15:40
# @Author  : Forec
# @File    : prob/__init__.py
# @Project : WildPointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn


from flask import Blueprint

prob = Blueprint('prob', __name__)

from . import views

from ..models import Permission


@prob.app_context_processor
def inject_permissions():
    return dict(Permission = Permission)