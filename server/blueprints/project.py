# -*- coding: utf-8 -*- 
# @Time : 2021/4/13 19:09
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : project.py 
# @Software: PyCharm


from flask import Blueprint, jsonify, request, send_file
from datetime import datetime

from server.algorithms.model import cls
from server.extensions import db
from server.models import User, Task, Project
from server.settings import ALLOWED_FILETYPES
from server.forms.project import CorrectForm
import os
import time

project_bp = Blueprint('project', __name__)


def is_allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_FILETYPES


# 上传项目
@project_bp.route('/upload', methods=['POST'])
def upload_file():
	user_id = int(request.form['user_id'])
	task_id = int(request.form['task_id'])
	file = request.files['file']

	filename = file.filename
	name = filename.split('.')[0]
	if is_allowed_file(filename) is False:
		return jsonify(code=400, message="File type is not allowed.")

	project = Project.query.order_by(-Project.id).limit(1).first()
	if project is None:
		max_project_id = 0
	else:
		max_project_id = project.id

	project = Project(name=name, user_id=user_id, task_id=task_id, commit_timestamp=datetime.utcnow())
	db.session.add(project)
	db.session.commit()

	task = Task.query.get(task_id)
	task.commit_num += 1
	db.session.commit()

	q_id = max_project_id + 1
	project = Project.query.get(q_id)

	path = os.path.join(os.getcwd(), 'files', str(user_id), str(project.id))
	if not os.path.exists(path):
		os.makedirs(path)

	file.save(path + '\\' + project.name + '.sb3')

	return jsonify(code=200, message="Upload success.", data={"id": project.id,
															  "name": project.name})


# 下载项目
@project_bp.route('/download/<project_id>', methods=['GET'])
def download_file(project_id):
	project = Project.query.get(project_id)

	path = os.path.join(os.getcwd(), 'files', str(project.user_id), str(project.id), project.name) + '.sb3'
	if not os.path.exists(path):
		return jsonify(code=400, message="File is not exist.")

	return send_file(path, as_attachment=True)


# 查询某个项目的评测结果
@project_bp.route('/<project_id>', methods=['GET'])
def show_project(project_id):
	project = Project.query.get(project_id)

	return jsonify(code=200, data={"id": project.id,
								   "name": project.name,
								   "score": project.score,
								   "comment": project.comment,
								   "logicality": project.logicality,
								   "workload": project.workload,
								   "complexity": project.complexity})


# 评测, 评测之后，相应任务的满分数会发生变化,评测过程大概30s
@project_bp.route('/evaluate/<project_id>', methods=['POST'])
def evaluate(project_id):
	project = Project.query.get(project_id)
	user_id = project.user_id
	project_name = project.name

	dirpath = os.path.join(os.getcwd(), 'files', str(user_id), str(project_id))

	# 评测
	score, logicality, workload, complexity = cls(dirpath, user_id, project_id, project_name)
	project.score = int(score)
	project.logicality = float(logicality)
	project.workload = float(workload)
	project.complexity = float(complexity)

	# TODO 要验一下score，如果score满分是4分的话，要score+=1

	# 生成评语
	overall = "【作业质量】"
	knowledge = "【知识点使用情况】"
	supply = "【补充】"
	if score == 5:
		overall += "优秀"
	elif score == 4 or score == 3:
		overall += "良好"
	else:
		overall += "一般"

	comment = overall + "\n" + knowledge + "\n" + supply
	project.comment = comment

	db.session.commit()

	return jsonify(code=200, message="Evaluate finished!")


# 老师批改项目（修改自动评测的结果）
@project_bp.route('/evaluate-correct', methods=['POST'])
def evaluate_correct():
	form = CorrectForm()

	project_id = form.id.data
	score = form.score.data
	comment = form.comment.data

	project = Project.query.get(project_id)
	project.score = score
	project.comment = comment
	db.session.commit()

	return jsonify(code=200, message="Edit group success.", data={"id": project.id,
																  "score": project.score,
																  "comment": project.comment})


# 删除作品
@project_bp.route('/delete', methods=['POST'])
def delete():
	return jsonify(code=200)
