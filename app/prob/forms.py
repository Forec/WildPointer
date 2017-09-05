# -*- coding: utf-8 -*-
# @Time    : 2017/9/5 16:41
# @Author  : Forec
# @File    : prob/forms.py
# @Software: Wild-Pointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn


from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import Required, Length
from ..models import Language


class SubmitCodeForm(Form):
    language = SelectField("选择语言", coerce=int)
    code = TextAreaField("代码", validators=[Required()])
    submit = SubmitField("提交")

    def __init__(self, *args, **kwargs):
        super(SubmitCodeForm, self).__init__(*args, **kwargs)
        self.language.choices = [(lan.id, lan.language)
                             for lan in Language.query.order_by(Language.language).all()]


class EditTaskForm(Form):
    title = StringField("标题", validators=[Required(), Length(0,64)])
    body = TextAreaField("内容", validators=[Required(), Length(1, 600)])
    submit = SubmitField("提交")


class SearchForm(Form):
    key = StringField('搜索', validators=[])


class ApplyForm(Form):
    suggestions = TextAreaField("你对此问题的建议/修正，bug也可在此提交给任务发布者", validators=[Required(), Length(1, 100)])
    submit = SubmitField("提交")
