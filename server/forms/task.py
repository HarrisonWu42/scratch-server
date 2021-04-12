# -*- coding: utf-8 -*- 
# @Time : 2021/4/7 17:58
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : task.py
# @Software: PyCharm


from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length


class TaskForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    answer_video_url = StringField('Answer Video Url', validators=[DataRequired(), Length(1, 120)])
    submit = SubmitField()


class EditTaskForm(FlaskForm):
    id = IntegerField('Id')
    name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    answer_video_url = StringField('Answer Video Url', validators=[DataRequired(), Length(1, 120)])
    submit = SubmitField()


class DeleteTaskForm(FlaskForm):
    id = IntegerField('Id')
    submit = SubmitField()


