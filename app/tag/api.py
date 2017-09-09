# -*- coding: utf-8 -*-
# @Time    : 2017/9/9 00:38
# @Author  : Forec
# @File    : tag/api.py
# @Project : WildPointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn


from flask import jsonify, request, render_template, flash
from flask_login import login_required, current_user

from . import tag as tagb
from .. import db
from ..models import Tag
from ..decorators import confirm_required
import json


@tagb.route('/recommend/<int:tag_count>', methods=['GET'])
def recommend(tag_count=15):
    hot_tags = Tag.query.order_by(Tag.count.asc()).slice(0, tag_count).all()
    return jsonify({
        'code': 1,
        'list': [tag.name for tag in hot_tags]
    })