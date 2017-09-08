# -*- coding: utf-8 -*-
# @Time    : 2017/9/7 14:59
# @Author  : Forec
# @File    : search/__init__.py
# @Project : WildPointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn


from flask import Blueprint

sea = Blueprint('sea', __name__)

from . import api, views
