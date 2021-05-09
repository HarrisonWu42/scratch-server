# -*- coding: utf-8 -*- 
# @Time : 2021/4/7 11:38
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : admin.py 
# @Software: PyCharm


from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class EditRoleForm(FlaskForm):
    role = StringField('Role')
    submit = SubmitField()