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


@tagb.route('/posts/<tag_name>', methods=['GET'])
def posts(tag_name):
    #TODO
    tag = Tag.query.get_or_404(name=tag_name)
    page = request.args.get('page', 1, type=int)
    pass


@tagb.route('/questions/<tag_name>', methods=['GET'])
def questions(tag_name):
    #TODO
    pass


@tagb.route('/all/<tag_name>', methods=['GET'])
def all(tag_name):
    #TODO
    pass
