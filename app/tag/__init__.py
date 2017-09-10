# -*- coding: utf-8 -*-
# @Time    : 2017/9/9 00:37
# @Author  : Forec
# @File    : tag/__init__.py
# @Project : WildPointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn


from flask import Blueprint

tag = Blueprint('tag', __name__)

from . import api
