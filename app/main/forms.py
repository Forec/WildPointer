# -*- coding: utf-8 -*-
# @Time    : 2017/9/5 09:21
# @Author  : Forec
# @File    : main/forms.py
# @Software: Wild-Pointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn


from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Required, Length, ValidationError
from flask_pagedown.fields import PageDownField

class HomeForm(FlaskForm):
    title = StringField("标题")
    body = PageDownField("正文（回车和多余空字符将被过滤）", validators=[Required()])
    submit = SubmitField('发布')
    def validate_body(self, field):
        if len(field.data) > 1500:
            raise ValidationError('正文过长，请限制在1400字内')

class CommentForm(FlaskForm):
    body = StringField('添加评论', validators=[Required()])
    submit = SubmitField('提交')

class SearchForm(FlaskForm):
    key = StringField('搜索', validators=[])

class EditApplyForm(FlaskForm):
    suggestions = TextAreaField("你当前此题的建议/修正（bug也可在此提交给任务发布者）", validators=[Required(), Length(1, 100)])
    submit = SubmitField("修改")
