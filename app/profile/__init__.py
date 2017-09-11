# -*- coding: utf-8 -*-
# @Time    : 2017/9/5 19:50
# @Author  : Forec
# @File    : profile/__init__.py
# @Project : WildPointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn

from flask import Blueprint

profile = Blueprint('profile', __name__)

from . import api

from ..models import Permission

@profile.app_context_processor
def inject_permissions():
    return dict(Permission = Permission)
