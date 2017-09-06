# -*- coding: utf-8 -*-
# @Time    : 2017/9/4 22:32
# @Author  : Forec
# @File    : config.py
# @Software: Wild-Pointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or \
                 '9d0e91f3372224b3ec7afec2' \
                 '4313e745efcf00ba4a5b767b' \
                 '35b17834d5f26efac197fd69' \
                 'd881dd92e629dbfdc2f1fbf6'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    WP_MAIL_SUBJECT_PREFIX = '[Wild-Pointer]'
    WP_MAIL_SENDER = os.environ.get('WP_MAIL_SENDER') or 'Wild-Pointer Admin <wild-pointer@forec.cn>'
    WP_ADMIN = os.environ.get('WP_ADMIN') or 'root'

    WP_POSTS_PER_PAGE = 20
    WP_FOLLOWERS_PER_PAGE = 20
    WP_COMMENTS_PER_PAGE = 15
    WP_QUESTIONS_PER_PAGE = 20
    WP_ANSWERS_PER_PAGE = 15
    PROFILE_WP_POSTS_PER_PAGE = 6
    PROFILE_WP_TASKS_PER_PAGE = 6
    EMAIL_ADMIN ='forec@bupt.edu.cn'
    @staticmethod
    def init_app(app):
        pass

class DevConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.exmail.qq.com'
    MAIL_PORT = 25 # SSL is 465
    MAIL_USE_TLS = True
    MAIL_USERNAME = "wild-pointer@forec.cn"
    MAIL_PASSWORD = os.environ.get('WP_MAIL_PASSWORD') or "WP-MAIL-ADMIN"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'tmp/debug.db')

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'tmp/test.db')

class ProductionConfig(Config):
    pass

config = {
    'dev': DevConfig,
    'test': TestConfig,
    'production': ProductionConfig,
    'default': DevConfig
}