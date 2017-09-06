# -*- coding: utf-8 -*-
# @Time    : 2017/9/6 10:04
# @Author  : Forec
# @File    : models/__init__.py
# @Project : WildPointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn


from .permission import Permission
from .anonymous import AnonymousUser
from .answer import Answer
from .role import Role
from .user import User
from .post import Post
from .tag import Tag
from .question import Question
from .message import Message
from .comment import PostComment, QuestionComment, AnswerComment
from .relationship import Follow, ContributeQuestions, LikeAnswers, UnLikeAnswers, \
    LikeQuestions, UnLikeQuestions, LikePosts
from .. import login_manager
from .. import db


login_manager.anonymous_user = AnonymousUser

db.event.listen(Post.body, 'set', Post.on_changed_body)

comment_table = {
    'post': PostComment,
    'answer': AnswerComment,
    'question': QuestionComment
}

material_table = {
    'post': Post,
    'answer': Answer,
    'question': Question,
    'comment': comment_table,
    'message': Message,
    'user': User,
    'role': Role,
    'permission': Permission
}