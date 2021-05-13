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
from server.models import Task, User, Project, Taskset
from math import ceil

from server.utils import bprojects2json, tasks2json

task_bp = Blueprint('task', __name__)


# 创建题目
@task_bp.route('/add', methods=['POST'])
def add():
	form = AddTaskForm()

	name = form.name.data
	description = form.description.data
	answer_video_url = form.answer_video_url.data
	teacher_id = form.teacher_id.data
	task = Task(name=name, description=description, teacher_id=teacher_id, answer_video_url=answer_video_url)

	db.session.add(task)
	db.session.commit()

	task = Task.query.filter_by(name=name).first()

	return jsonify(code=200, message="Add task success.", data={"id": task.id,
																"name": task.name,
																"description": task.description,
																"teacher_id": task.teacher_id,
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


@task_bp.route('/<task_id>', methods=['GET'])
def show_task(task_id):
	task = Task.query.get(task_id)

	return jsonify(code=200, data={"id": task.id,
								   "name": task.name,
								   "description": task.description,
								   "answer_video_url": task.answer_video_url})


# 查看某人某任务的所有提交列表
@task_bp.route('/project/<user_id>/<task_id>', methods=['GET'])
def show_projects(user_id, task_id):
	user = User.query.get(user_id)
	projects = Project.query.filter(Project.user_id == user_id, Project.task_id == task_id)\
		.order_by(Project.commit_timestamp.desc()).all()
	data = bprojects2json(projects)

	return jsonify(code=200, data=data)


# 查看所有任务
@task_bp.route('/all/<offset>/<page_size>', methods=['GET'])
def show_all_tasks(offset, page_size):
	page_size = int(page_size)
	offset = int(offset)

	tasks = Task.query.all()

	json_array = []
	for task in tasks:
		teacher_id = task.teacher_id
		teacher = User.query.get(teacher_id)
		task_obj = {"id": task.id,
				   "name": task.name,
				   "description": task.description,
					"teacher": teacher.name}
		json_array.append(task_obj)

	page_tasks = json_array[(offset - 1) * page_size: offset * page_size]
	total_pages = ceil(len(tasks) / page_size)

	data = {"tasksets": page_tasks, 'total_pages': total_pages}

	return jsonify(code=200, data=data)


# 为题目集分配题目
@task_bp.route('/assign2taskset', methods=['POST'])
def assign2taskset():
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