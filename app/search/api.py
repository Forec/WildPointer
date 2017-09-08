# -*- coding: utf-8 -*-
# @Time    : 2017/9/7 14:59
# @Author  : Forec
# @File    : search/api.py
# @Project : WildPointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn


from flask import request, jsonify
from . import sea
from ..models import Post, Question, Answer
import json
