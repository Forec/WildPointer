# -*- coding: utf-8 -*-
# @Time    : 2017/9/6 23:21
# @Author  : Forec
# @File    : post/forms.py
# @Project : WildPointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn


from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from flask_pagedown.fields import PageDownField


class PostEditForm(FlaskForm):
    title = StringField("标题")
    body = PageDownField("正文（回车和多余空字符将被过滤）", validators=[DataRequired()])
    tags = StringField("标签（请用半角逗号分隔）")
    submit = SubmitField('发布')

    def validate_body(self, field):
        if len(field.data) > 1500:
            raise ValidationError('正文过长，请限制在1400字内')

    def validate_tags(self, field):
        tags_string = field.data
        tags_list = [tag_string.strip() for tag_string in tags_string.split(',')]
        if len(tags_list) > 5:
            raise ValidationError('标签过长，每个标签不可超过 6 个字符，不可超过 5 个标签')
        for tag_string in tags_list:
            if len(tag_string) > 6:
                raise ValidationError('标签过长，每个标签不可超过 6 个字符，不可超过 5 个标签')
