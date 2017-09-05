# -*- coding: utf-8 -*-
# @Time    : 2017/9/5 18:54
# @Author  : Forec
# @File    : auth/__init__.py
# @Software: Wild-Pointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn


from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views