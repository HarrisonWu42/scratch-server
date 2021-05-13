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
from server.models import Taskset, User, Task, Project, Group
from server.utils import tasks2json, taskset2json, btasks2json

taskset_bp = Blueprint('taskset', __name__)


# 创建题目集
@taskset_bp.route('/add', methods=['POST'])
def add():
	form = AddTasksetForm()

	name = form.name.data
	type = form.type.data
	teacher_id = form.teacher_id.data

	taskset = Taskset(name=name, type=type, teacher_id=teacher_id)

	db.session.add(taskset)
	db.session.commit()

	taskset = Taskset.query.filter_by(name=name).first()

	return jsonify(code=200, message="Add taskset success.", data={"id": taskset.id,
																   "name": taskset.name,
																   "type": taskset.type,
																   "teacher_id": teacher_id})


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
	taskset_id = int(taskset_id)

	taskset = Taskset.query.get(taskset_id)
	tasks = taskset.tasks
	task_id_lst = list()
	for task in tasks:
		task_id_lst.append(task.id)

	projects = Project.query.filter_by(user_id=user_id).filter(Project.task_id.in_(task_id_lst)).all()

	score = 0
	for project in projects:
		score += project.score

	total_score = len(projects) * 5

	return jsonify(code=200, data={"score": score, "total_score": total_score})


# 显示某人的题目集
# 访客 user_id = 0, 用户 user_id = 真实user_id
@taskset_bp.route('/<user_id>/<offset>/<page_size>', methods=['GET'])
def show_tasksets(user_id, offset, page_size):
	user_id = int(user_id)
	page_size = int(page_size)
	offset = int(offset)

	# 固定题目集
	common_tasksets = Taskset.query.filter_by(type=1).all()

	# 私人题目集
	user_tasksets = set()
	if user_id != 0:
		user = User.query.get(user_id)
		if user.role.name == "Teacher":
			user_tasksets = Taskset.query.filter_by(teacher_id=user_id, type=0).all()
			user_tasksets = set(user_tasksets)
		elif user.role.name == "Student":
			groups = user.groups
			for group in groups:
				group_tasksets = group.tasksets
				user_tasksets = set.union(user_tasksets, group_tasksets)

	tasksets = set.union(set(common_tasksets), user_tasksets)  # 任务集合集
	tasksets = list(tasksets)

	page_tasksets = tasksets[(offset - 1) * page_size: offset * page_size]

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


# 查询固定任务集（题库）
@taskset_bp.route('/common/<offset>/<page_size>', methods=['GET'])
def show_common_tasksets(offset, page_size):
	page_size = int(page_size)
	offset = int(offset)

	tasksets = Taskset.query.filter_by(type=1).all()
	page_tasksets = tasksets[(offset - 1) * page_size: offset * page_size]
	total_pages = ceil(len(tasksets) / page_size)

	data = taskset2json(page_tasksets)
	data['total_pages'] = total_pages

	return jsonify(code=200, data=data)


# 查询私有任务集（题库）
@taskset_bp.route('/private/<user_id>/<offset>/<page_size>', methods=['GET'])
def show_private_tasksets(user_id, offset, page_size):
	user_id = int(user_id)
	page_size = int(page_size)
	offset = int(offset)

	tasksets = Taskset.query.filter_by(teacher_id=user_id, type=0).all()

	page_tasksets = tasksets[(offset - 1) * page_size: offset * page_size]
	total_pages = ceil(len(tasksets) / page_size)

	data = taskset2json(page_tasksets)
	data['total_pages'] = total_pages

	return jsonify(code=200, data=data)


# 查看老师的私人任务集，要显示这个任务集对于这个班级是否已经分配
@taskset_bp.route('/query_before_assign/<user_id>/<group_id>', methods=['GET'])
def query_before_assign(user_id, group_id):
	teacher_id = int(user_id)
	group_id = int(group_id)

	# 老师的所有私人任务集
	tasksets = Taskset.query.filter_by(teacher_id=teacher_id, type=0).all()
	group = Group.query.get(group_id)

	json_array = []
	for taskset in tasksets:
		if taskset in group.tasksets:
			is_opened = "已授权"
		else:
			is_opened = "未授权"
		taskset_obj = {"id": taskset.id,
					   "name": taskset.name,
					   "is_opened": is_opened}
		json_array.append(taskset_obj)
	json_dic = {"tasksets": json_array}

	return jsonify(code=200, message="Assign task success.", data=json_dic)


# 为班级分配题目集
@taskset_bp.route('/assign2group/<group_id>/<taskset_id>', methods=['POST'])
def assign2group(group_id, taskset_id):
	group_id = int(group_id)
	taskset_id = int(taskset_id)

	group = Group.query.get(group_id)
	taskset = Taskset.query.get(taskset_id)

	if taskset not in group.tasksets:
		group.tasksets.append(taskset)
		msg = "Assign taskset success."
	else:
		group.tasksets.remove(taskset)
		msg = "Cancel assign taskset success."

	db.session.commit()

	return jsonify(code=200, message=msg, data={"group_id": group_id,
												"group_name": group.name,
												"taskset_id": taskset.id,
												"taskset_name": taskset.name})
