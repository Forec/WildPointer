# -*- coding: utf-8 -*-
# @Time    : 2017/9/5 19:11
# @Author  : Forec
# @File    : verifiers.py
# @Project : WildPointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn

import re

def verify_email(email):
    if len(email) > 7 and \
        re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
        return True
    return False

def verify_nickname(nickname):
    invalid = ['?', '/', '=', '>', '<', '!', ',', ';', '.', '\\']
    for inv in invalid:
        if inv in nickname:
            return False
    return True