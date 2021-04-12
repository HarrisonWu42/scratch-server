# -*- coding: utf-8 -*- 
# @Time : 2021/4/7 17:57
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : task.py
# @Software: PyCharm
from flask import Blueprint, jsonify, request

from server.extensions import db
from server.forms.task import TaskForm, DeleteTaskForm, EditTaskForm
from server.models import Task
from server.utils import tasks2json

task_bp = Blueprint('task', __name__)


# 显示所有任务, 这个接口后面可能还要修改
@task_bp.route('/all/<offset>/<per_page>', methods=['GET'])
def show_tasks(offset, per_page):
	per_page = int(per_page)
	offset = int(offset)

	tasks = Task.query.limit(per_page).offset((offset - 1) * per_page)

	data = tasks2json(tasks)

	# 提交数

	# 满分数

	# 满分率

	return jsonify(code=200, data=data)


# 发布任务
@task_bp.route('/add', methods=['POST'])
def add():
	form = TaskForm()

	name = form.name.data
	answer_video_url = form.answer_video_url.data
	task = Task(name=name, answer_video_url=answer_video_url)

	db.session.add(task)
	db.session.commit()

	task = Task.query.filter_by(name=name).first()
	id = task.id

	return jsonify(code=200, message="Add task success.", data={"id": id,
																"name": name,
																"answer_video_url": answer_video_url})


# 修改任务
@task_bp.route('/edit', methods=['POST'])
def edit():
	form = EditTaskForm()

	id = form.id.data
	name = form.name.data
	answer_video_url = form.answer_video_url.data

	task = Task.query.get(id)

	task.name = name
	task.answer_video_url = answer_video_url

	db.session.commit()

	return jsonify(code=200, message="Add task success.", data={"id": id,
																"name": name,
																"answer_video_url": answer_video_url})


# 删除任务
@task_bp.route('/delete', methods=['POST'])
def delete():
	form = DeleteTaskForm()

	id = form.id.data

	task = Task.query.get(id)

	db.session.delete(task)
	db.session.commit()

	return jsonify(code=200, message="Delete success", data={"id": task.id,
																"name": task.name,
																"answer_video_url": task.answer_video_url})

