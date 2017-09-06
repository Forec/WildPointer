# -*- coding: utf-8 -*-
# @Time    : 2017/9/7 00:31
# @Author  : Forec
# @File    : message/__init__.py
# @Project : WildPointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn


from flask import Blueprint

message = Blueprint('message', __name__)

from . import views, api
