# -*- coding: utf-8 -*- 
# @Time : 2021/4/7 17:58
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : task.py
# @Software: PyCharm


from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FieldList, FormField
from wtforms.validators import DataRequired, Length


class AddTaskForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    answer_video_url = StringField('Answer Video Url', validators=[DataRequired(), Length(1, 120)])
    submit = SubmitField()


class EditTaskForm(FlaskForm):
    id = IntegerField('id')
    name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    answer_video_url = StringField('Answer Video Url', validators=[DataRequired(), Length(1, 120)])
    submit = SubmitField()


class DeleteTaskForm(FlaskForm):
    id = IntegerField('id')
    submit = SubmitField()