# -*- coding: utf-8 -*- 
# @Time : 2021/4/7 17:57
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : task.py
# @Software: PyCharm
from flask import Blueprint, jsonify

from server.extensions import db
from server.forms.task import TaskForm
from server.models import Task

task_bp = Blueprint('task', __name__)


# 显示所有任务
@task_bp.route('/all', methods=['GET'])
def show_tasks():
	tasks = Task.query.all()


	return jsonify(code=200)


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
																"name": name})


# # 修改任务
# @task_bp.route('/edit', methods=['POST'])
# def edit():
# 	form = TaskForm()
#
# 	name = form.name.data
# 	answer_video_url = form.answer_video_url.data
#
# 	task = Task.query.filter_by(name=name).first()
# 	task.answer_video_url = answer_video_url
#
# 	db.commit()
#
#
#
#
# # 删除任务
# @task_bp.route('/delete', methods=['POST', 'GET'])
# def delete():
# 	print(11111111111111)
