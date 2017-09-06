# -*- coding: utf-8 -*-
# @Time    : 2017/9/6 09:49
# @Author  : Forec
# @File    : models/permission.py
# @Project : WildPointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn


class Permission:
    FOLLOW = 0x01  # focus other users
    COMMENT = 0x02  # comment on other users' articles
    WRITE_POSTS = 0x04  # write articles
    MODERATE_COMMENTS = 0x08  # moderate users' comments
    MODERATE_ALL = 0x10
    ADMINISTER = 0x80  # administer
