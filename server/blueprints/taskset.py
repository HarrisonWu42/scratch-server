# -*- coding: utf-8 -*- 
# @Time : 2021/4/14 12:13
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : taskset.py 
# @Software: PyCharm
import json
from math import ceil

from flask import Blueprint, jsonify, request

from server.extensions import db
from server.forms.taskset import AddTasksetForm, EditTasksetForm, DeleteTaskForm
from server.models import Taskset, User, Task
from server.utils import tasks2json, taskset2json

taskset_bp = Blueprint('taskset', __name__)


# 创建题目集
@taskset_bp.route('/add', methods=['POST'])
def add():
	form = AddTasksetForm()

	name = form.name.data
	type = form.type.data

	taskset = Taskset(name=name, type=type)

	db.session.add(taskset)
	db.session.commit()

	taskset = Taskset.query.filter_by(name=name).first()

	return jsonify(code=200, message="Add taskset success.", data={"id": taskset.id,
																   "name": taskset.name,
																   "type": taskset.type})


# 修改题目集
@taskset_bp.route('/edit', methods=['POST'])
def edit():
	form = EditTasksetForm()

	id = form.id.data
	name = form.name.data
	type = form.type.data

	taskset = Taskset.query.get(id)

	taskset.name = name
	taskset.type = type

	db.session.commit()

	return jsonify(code=200, message="Edit taskset success.", data={"id": taskset.id,
																   "name": taskset.name,
																   "type": taskset.type})


# 删除题目集
@taskset_bp.route('/delete', methods=['POST'])
def delete():
	form = DeleteTaskForm()

	id = form.id.data

	taskset = Taskset.query.get(id)

	db.session.delete(taskset)
	db.session.commit()

	return jsonify(code=200, message="Delete taskset success", data={"id": taskset.id,
																   "name": taskset.name,
																   "type": taskset.type})


# 为题目集分配题目
@taskset_bp.route('/assign', methods=['POST'])
def assign():
	data = json.loads(bytes.decode(request.data))
	taskset_id = data["taskset_id"]
	task_id_list = data['tasks']

	taskset = Taskset.query.get(taskset_id)
	for task_id in task_id_list:
		task = Task.query.get(task_id)
		taskset.tasks.append(task)

	db.session.commit()

	tasks = taskset.tasks
	data = tasks2json(tasks)
	data['taskset_id'] = taskset.id
	data['taskset_name'] = taskset.name

	return jsonify(code=200, message="Assign task success.", data=data)


# 查询题目集的的所有题目
@taskset_bp.route('/task/<taskset_id>', methods=['GET'])
def show_tasks(taskset_id):
	taskset_id = int(taskset_id)

	taskset = Taskset.query.get(taskset_id)
	tasks = taskset.tasks

	data = tasks2json(tasks)

	return jsonify(code=200, data=data)


# 查询某人某题目集的得分（得分/总分）
@taskset_bp.route('/<user_id>/<taskset_id>', methods=['GET'])
def show_taskset_score(user_id, taskset_id):
	user_id = int(user_id)
	user = User.query.get(user_id)
	taskset_id = int(taskset_id)

	taskset = Taskset.query.get(taskset_id)
	tasks = taskset.tasks

	data = tasks2json(tasks)

	return jsonify(code=200, data=data)


# 显示某人的题目集
# 访客 user_id = 0, 用户 user_id = 真实user_id
@taskset_bp.route('/<user_id>/<offset>/<page_size>', methods=['GET'])
def show_tasksets(user_id, offset, page_size):
	user_id = int(user_id)
	page_size = int(page_size)
	offset = int(offset)

	# 固定题目集
	common_tasksets = Taskset.query.filter_by(type=1).all()

	# 个人题目集
	user_tasksets = list()
	if user_id != 0:
		user = User.query.get(user_id)
		groups = user.groups
		for group in groups:
			taskset = group.tasksets
			user_tasksets = user_tasksets + taskset

	tasksets = common_tasksets + user_tasksets  # 任务集合集
	page_tasksets = tasksets[(offset-1) * page_size: offset * page_size]

	# 总页数
	total_pages = ceil(len(tasksets) / page_size)

	data = taskset2json(page_tasksets)
	data['total_pages'] = total_pages
	if user_id == 0:
		data['user_id'] = 0
		data['user_name'] = "访客"
	else:
		data['user_id'] = user.id
		data['user_name'] = user.name

	return jsonify(code=200, data=data)



# # 查询题目集的的所有题目（分页版本）
# @taskset_bp.route('/task/<taskset_id>/<offset>/<page_size>', methods=['GET'])
# def show_tasks(taskset_id, offset, page_size):
# 	task_id = int(taskset_id)
# 	page_size = int(page_size)
# 	offset = int(offset)
#
# 	taskset = Taskset.query.get(taskset_id)
# 	tasks = taskset.tasks
# 	page_tasks = tasks[(offset-1) * page_size: offset * page_size]
#
# 	total_pages = ceil((len(tasks) + page_size - 1) / page_size)
#
# 	data = tasks2json(page_tasks)
# 	data['total_pages'] = total_pages
#
# 	# 显示个人的总分和得分
#
# 	return jsonify(code=200, data=data)