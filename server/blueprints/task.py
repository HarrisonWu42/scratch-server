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
from server.models import Task, Group, User
from server.utils import tasks2json, groups2json
from math import ceil

task_bp = Blueprint('task', __name__)


# 显示任务集
@task_bp.route('/tasksets/<user_id>/<offset>/<page_size>', methods=['GET'])
def show_tasksets(user_id, offset, page_size):
	page_size = int(page_size)
	offset = int(offset)

	common_taskset = Group.query.filter_by(type=2).all()  # 固定任务集
	user = User.query.get(user_id)
	user_tasksets = user.groups  # 个人任务集
	tasksets = common_taskset + user_tasksets  # 任务集合集
	page_tasksets = tasksets[(offset-1) * page_size: offset * page_size]

	# 总页数
	total_pages = ceil(len(tasksets) / page_size)

	data = groups2json(page_tasksets)
	data['total_pages'] = total_pages
	data['user_id'] = user.id
	data['user_name'] = user.name

	return jsonify(code=200, data=data)


# 显示题目集的所有题目（后续还需要修改）
@task_bp.route('/taskset/<group_id>/<offset>/<page_size>', methods=['GET'])
def show_tasks(group_id, offset, page_size):
	page_size = int(page_size)
	offset = int(offset)

	group = Group.query.get(group_id)
	tasks = group.tasks
	page_tasks = tasks[(offset-1) * page_size: offset * page_size]

	total_pages = ceil((len(tasks) + page_size - 1) / page_size)

	data = tasks2json(page_tasks)
	data['total_pages'] = total_pages

	# 提交数

	# 满分数

	# 满分率

	return jsonify(code=200, data=data)


# 发布任务
@task_bp.route('/add', methods=['POST'])
def add():
	form = AddTaskForm()

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

	return jsonify(code=200, message="Edit task success.", data={"id": id,
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

	return jsonify(code=200, message="Delete task success", data={"id": task.id,
																  "name": task.name,
																  "answer_video_url": task.answer_video_url})


# 为某个班组（任务集）选择任务
@task_bp.route('/assign', methods=['POST'])
def assign():
	data = json.loads(bytes.decode(request.data))
	group_id = data["group_id"]
	task_id_list = data['tasks']

	group = Group.query.get(group_id)
	for task_id in task_id_list:
		task = Task.query.get(task_id)
		group.tasks.append(task)

	db.session.commit()

	tasks = group.tasks
	data = tasks2json(tasks)
	data['group_id'] = group.id
	data['group_name'] = group.name

	return jsonify(code=200, message="Assign task success.", data=data)