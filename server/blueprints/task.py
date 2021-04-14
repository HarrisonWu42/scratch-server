# -*- coding: utf-8 -*- 
# @Time : 2021/4/7 17:57
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : task.py
# @Software: PyCharm
import json

from flask import Blueprint, jsonify, request

from server.extensions import db
from server.forms.task import AddTaskForm, EditTaskForm, DeleteTaskForm
from server.models import Task
from math import ceil

task_bp = Blueprint('task', __name__)


# 创建题目
@task_bp.route('/add', methods=['POST'])
def add():
	form = AddTaskForm()

	name = form.name.data
	description = form.description.data
	answer_video_url = form.answer_video_url.data
	task = Task(name=name, description=description, answer_video_url=answer_video_url)

	db.session.add(task)
	db.session.commit()

	task = Task.query.filter_by(name=name).first()

	return jsonify(code=200, message="Add task success.", data={"id": task.id,
																"name": task.name,
																"description": task.description,
																"answer_video_url": task.answer_video_url})


# 修改题目
@task_bp.route('/edit', methods=['POST'])
def edit():
	form = EditTaskForm()

	id = form.id.data
	name = form.name.data
	description = form.description.data
	answer_video_url = form.answer_video_url.data

	task = Task.query.get(id)
	if task is None:
		return jsonify(code=400, message="Task not exist.")

	task.name = name
	task.description = description
	task.answer_video_url = answer_video_url

	db.session.commit()

	return jsonify(code=200, message="Edit task success.", data={"id": task.id,
																"name": task.name,
																"description": task.description,
																"answer_video_url": task.answer_video_url})


# 删除题目
@task_bp.route('/delete', methods=['POST'])
def delete():
	form = DeleteTaskForm()

	id = form.id.data

	task = Task.query.get(id)

	if task is None:
		return jsonify(code=400, message="Task not exist.")

	db.session.delete(task)
	db.session.commit()

	return jsonify(code=200, message="Delete task success", data={"id": task.id,
																  "name": task.name,
																  "description": task.description,
																  "answer_video_url": task.answer_video_url})