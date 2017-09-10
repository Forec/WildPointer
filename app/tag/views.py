# -*- coding: utf-8 -*-
# @Time    : 2017/9/9 00:38
# @Author  : Forec
# @File    : tag/views.py
# @Project : WildPointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn


from flask import request, render_template, flash
from flask_login import login_required, current_user

from . import tag as tagb
from .. import db
from ..models import Tag
from ..decorators import confirm_required


@tagb.route('/posts/<tag_list>', methods=['GET'])
def posts(tag_list):
    #TODO
    pass


@tagb.route('/questions/<tag_list>', methods=['GET'])
def questions(tag_list):
    #TODO
    pass


@tagb.route('/all/<tag_list>', methods=['GET'])
def all(tag_name):
    #TODO
    pass
