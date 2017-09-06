# -*- coding: utf-8 -*-
# @Time    : 2017/9/6 09:49
# @Author  : Forec
# @File    : models/role.py
# @Project : WildPointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn


from .permission import Permission
from .. import db


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    default = db.Column(db.Boolean, default=False)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            '未激活用户': (0x00, True),
            '普通用户': (Permission.FOLLOW |
                     Permission.COMMENT |
                     Permission.WRITE_POSTS, False),
            '评论管理员': (Permission.FOLLOW |
                      Permission.COMMENT |
                      Permission.WRITE_POSTS |
                      Permission.MODERATE_COMMENTS, False),
            '问题管理员': (Permission.COMMENT |
                      Permission.WRITE_POSTS |
                      Permission.MODERATE_ALL, False),
            '超级管理员': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name
