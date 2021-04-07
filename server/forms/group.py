# -*- coding: utf-8 -*- 
# @Time : 2021/4/7 18:26
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : group.py 
# @Software: PyCharm


from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, HiddenField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional, Regexp


class GroupForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(1, 254)])
    type = BooleanField('Open')
    teacher_name = StringField('TeacherName', validators=[DataRequired(), Length(1, 30)])
    submit = SubmitField()


class EditGroupForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(1, 254)])
    submit = SubmitField()