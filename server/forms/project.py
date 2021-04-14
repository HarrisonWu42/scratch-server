# -*- coding: utf-8 -*- 
# @Time : 2021/4/13 22:33
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : project.py 
# @Software: PyCharm


from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional, Regexp


class ProjectForm(FlaskForm):
	name = StringField('name', validators=[DataRequired(), Length(1, 30)])
	user_id = IntegerField('user_id')
	task_id = IntegerField('task_id')
	teacher_id = IntegerField('teacher_id')
	submit = SubmitField()


class CorrectForm(FlaskForm):
	id = IntegerField('id')
	score = IntegerField('id')
	submit = SubmitField()
