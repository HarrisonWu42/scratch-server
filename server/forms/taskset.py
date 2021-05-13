# -*- coding: utf-8 -*- 
# @Time : 2021/4/14 13:35
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : taskset.py 
# @Software: PyCharm


from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length


class AddTasksetForm(FlaskForm):
    name = StringField('name', validators=[DataRequired(), Length(1, 30)])
    type = IntegerField('type')
    teacher_id = IntegerField('teacher_id')
    submit = SubmitField()


class EditTasksetForm(FlaskForm):
    id = IntegerField('id')
    name = StringField('name', validators=[DataRequired(), Length(1, 30)])
    type = IntegerField('type')
    submit = SubmitField()


class DeleteTaskForm(FlaskForm):
    id = IntegerField('id')
    submit = SubmitField()


class DeleteTaskTasksetForm(FlaskForm):
    task_id = IntegerField('task_id')
    taskset_id = IntegerField('taskset_id')
    submit = SubmitField()
