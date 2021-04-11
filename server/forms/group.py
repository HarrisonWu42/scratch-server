# -*- coding: utf-8 -*- 
# @Time : 2021/4/7 18:26
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : group.py 
# @Software: PyCharm


from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional, Regexp


class GroupForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(1, 254)])
    teacher_id = IntegerField('TeacherId')
    submit = SubmitField()


class EditGroupForm(FlaskForm):
    id = IntegerField('Id')
    name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(1, 254)])
    submit = SubmitField()


class CloseGroupForm(FlaskForm):
    id = IntegerField('Id')
    submit = SubmitField()


class DeleteGroupForm(FlaskForm):
    id = IntegerField('Id')
    submit = SubmitField()


class InviteGroupForm(FlaskForm):
    user_id = IntegerField('user_id')
    invite_code = StringField('invite_code', validators=[DataRequired(), Length(6, 6)])
    submit = SubmitField()