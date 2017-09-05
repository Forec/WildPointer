# -*- coding: utf-8 -*-
# @Time    : 2017/9/5 00:27
# @Author  : Forec
# @File    : main/__init__.py
# @Software: Wild-Pointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn


from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors

from ..models import Permission


@main.app_context_processor
def inject_permissions():
    return dict(Permission = Permission)