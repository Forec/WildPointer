# -*- coding: utf-8 -*-
# @Time    : 2017/9/5 19:53
# @Author  : Forec
# @File    : profile/forms.py
# @Project : WildPointer
# @license : Copyright(C), Forec
# @Contact : forec@bupt.edu.cn


from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField
from wtforms.validators import Required, Length, Email, Regexp, ValidationError
from ..models import Role, User

class EditProfileForm(Form):
    name = StringField('昵称', validators=[Length(0, 64)])
    location = StringField('地址', validators=[Length(0, 64)])
    contactE = StringField('联系方式', validators=[Length(0,64)])
    about_me = TextAreaField('关于我')
    submit = SubmitField('提交')

class EditProfileAdminForm(Form):
    email = StringField('电子邮箱', validators=[Required(), Length(5,64), Email()])
    username = StringField('用户名', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_]*$', 0,
                                          '用户名仅能包含字母、数字和下划线')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('身份', coerce=int)
    name = StringField('昵称', validators=[Length(0, 64)])
    contactE = StringField('联系方式', validators=[Length(0,64)])
    location = StringField('位置', validators=[Length(0, 64)])
    about_me = TextAreaField('关于我')
    submit = SubmitField('提交')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已注册.')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户名已被使用.')
