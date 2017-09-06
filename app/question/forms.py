# -*- coding: utf-8 -*-
# @Time    : 2017/9/5 16:41
# @Author  : Forec
# @File    : question/forms.py
# @Software: Wild-Pointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn


from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class SubmitQuestionForm(Form):
    title = StringField('标题', validators=[DataRequired(), Length(0, 64)])
    body = TextAreaField("详细说明", validators=[Length(0, 600)])
    submit = SubmitField("提交")

    def __init__(self, *args, **kwargs):
        super(SubmitQuestionForm, self).__init__(*args, **kwargs)


class EditQuestionForm(Form):
    title = StringField("标题", validators=[DataRequired(), Length(0, 64)])
    body = TextAreaField("内容", validators=[Length(0, 600)])
    submit = SubmitField("提交")


class SearchForm(Form):
    key = StringField('搜索', validators=[])
