# -*- coding: utf-8 -*- 
# @Time : 2021/4/7 18:26
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : group.py 
# @Software: PyCharm
import json
import random
from math import ceil
import flask_excel as excel
import pandas as pd
import xlsxwriter
from flask import Blueprint, jsonify, request, make_response
from werkzeug.security import generate_password_hash

from server.extensions import db
from server.forms.group import GroupForm, EditGroupForm, CloseGroupForm, DeleteGroupForm, InviteGroupForm, KickGroupForm
from server.models import Group, User, Task, Project, Taskset
from server.utils import groups2json, users2json, taskset2json

group_bp = Blueprint('group', __name__)


# 显示某个老师的班组
@group_bp.route('/teacher/<teacher_id>', methods=['GET'])
def show_tasks(teacher_id):
	teacher_id = int(teacher_id)
	groups = Group.query.filter_by(teacher_id=teacher_id).all()

	data = groups2json(groups)
	data['total'] = len(groups)

	return jsonify(code=200, data=data)


# 显示某个班组的所有学生
@group_bp.route('/<group_id>/<offset>/<page_size>', methods=['GET'])
def show_students(group_id, offset, page_size):
	id = int(group_id)
	page_size = int(page_size)
	offset = int(offset)

	group = Group.query.get(id)
	users = group.users  # 所有users
	page_users = users[(offset - 1) * page_size: offset * page_size]

	total_pages = ceil(len(users) / page_size)

	data = users2json(page_users)
	data['total_pages'] = total_pages

	return jsonify(code=200, data=data)


# 创建班组
@group_bp.route('/add', methods=['POST'])
def add():
	form = GroupForm()

	name = form.name.data
	description = form.description.data
	teacher_id = form.teacher_id.data

	invite_code = "".join(item for item in random.sample('0123456789', 6))
	while Group.query.filter_by(invite_code=invite_code).first() is not None:
		invite_code = "".join(item for item in random.sample('0123456789', 6))

	group = Group(name=name, description=description, type=1, teacher_id=teacher_id, invite_code=invite_code)

	db.session.add(group)
	db.session.commit()

	group = Group.query.filter_by(name=name).first()

	return jsonify(code=200, message="Add group success.", data={"id": group.id,
																 "name": group.name,
																 "description": group.description,
																 "type": group.type,
																 "teacher_id": group.teacher_id,
																 "invite_code": group.invite_code})


# 修改班组
@group_bp.route('/edit', methods=['POST'])
def edit():
	form = EditGroupForm()

	id = form.id.data
	name = form.name.data
	description = form.description.data

	group = Group.query.get(id)

	group.name = name
	group.description = description

	db.session.commit()

	return jsonify(code=200, message="Edit group success.", data={"id": group.id,
																  "name": group.name,
																  "description": group.description,
																  "type": group.type,
																  "teacher_id": group.teacher_id,
																  "invite_code": group.invite_code})


# 删除班组
@group_bp.route('/delete', methods=['POST'])
def delete():
	form = DeleteGroupForm()

	id = form.id.data

	group = Group.query.get(id)

	db.session.delete(group)
	db.session.commit()

	return jsonify(code=200, message="Delete group success.", data={"id": group.id,
																	"name": group.name,
																	"description": group.description,
																	"type": group.type,
																	"teacher_id": group.teacher_id,
																	"invite_code": group.invite_code})


# 通过邀请码邀请用户加入班组
@group_bp.route('/invite', methods=['POST'])
def invite():
	form = InviteGroupForm()

	user_id = form.user_id.data
	invite_code = form.invite_code.data

	group = Group.query.filter_by(invite_code=invite_code).first()
	user = User.query.get(user_id)
	group.users.append(user)

	db.session.commit()

	return jsonify(code=200, message="Invite success.", data={"user_id": user.id,
															  "user_name": user.name,
															  "email": user.email,
															  "group_id": group.id,
															  "group_name": group.name})


# 删除某个班组的某个学生
@group_bp.route('/kick', methods=['POST'])
def kick():
	form = KickGroupForm()

	user_id = form.user_id.data
	group_id = form.group_id.data

	group = Group.query.get(group_id)
	user = User.query.get(user_id)
	group.users.remove(user)

	db.session.commit()

	return jsonify(code=200, message="Invite success.", data={"user_id": user.id,
															  "user_name": user.name,
															  "email": user.email,
															  "group_id": group.id,
															  "group_name": group.name})


# 通过导入excel将学生一键加入班级
@group_bp.route('/import_excel/<group_id>', methods=['POST'])
def import_student_from_excel(group_id):
	file = request.files['file']

	print('file', type(file), file)
	print(file.filename)  # 打印文件名

	data = pd.read_excel(file)
	column_names = data.columns.values.tolist()
	column_format = ["用户名", "邮箱"]
	if column_names != column_format:
		return jsonify(code=402, message="Excel header error.")

	nrows, ncols = data.shape

	default_password = generate_password_hash("123456")

	try:
		db.session.execute(
			User.__table__.insert(),
			[{"name": row['用户名'], "email": row['邮箱'], "password_hash": default_password, "role_id":1} for idx, row in
			 data.iterrows()]
		)
		db.session.commit()

		group = Group.query.get(group_id)
		for email in data['邮箱']:
			user = User.query.filter_by(email=email).first()
			group.users.append(user)
		db.session.commit()

		return jsonify(code=200, message="Import success.")
	except Exception as e:
		return jsonify(code=403, message="Import students error.", exception=e)


# 导出班级的学生成绩   user_name, email, task_name, project_name, score, comment(后续可能还要加上传时间和批改时间)
@group_bp.route('/output_excel/<group_id>', methods=['GET'])
def output_excel(group_id):
	group = Group.query.get(group_id)

	task_id_list = list()
	tasksets = group.tasksets
	for taskset in tasksets:
		tasks = taskset.tasks
		for task in tasks:
			task_id_list.append(task.id)

	user_id_list = list()
	users = group.users
	for user in users:
		user_id_list.append(user.id)

	q = db.session.query(
		User.name.label('用户名'),
		User.email.label('邮箱'),
		Task.name.label('题目名'),
		Project.name.label('作品名'),
		Project.commit_timestamp.label('提交时间'),
		Project.score.label('评分'),
		Project.comment.label('评语')
	).filter(Project.user_id == User.id, Project.task_id == Task.id) \
		.filter(User.id.in_(user_id_list)) \
		.filter(Task.id.in_(task_id_list)) \
		.order_by(User.id.asc()).order_by(Task.id.asc())

	query_sets = q.all()

	file_name = group.name + '.xlsx'
	file_data = excel.make_response_from_query_sets(
		query_sets,
		column_names=[
			'用户名',
			'邮箱',
			'题目名',
			'作品名',
			'提交时间',
			'评分',
			'评语'
		],
		file_type='xlsx',
		file_name=file_name
	)

	return file_data


# # 显示某个老师的班组(分页)
# @group_bp.route('/teacher/<teacher_id>/<offset>/<page_size>', methods=['GET'])
# def show_tasks(teacher_id, offset, page_size):
#     teacher_id = int(teacher_id)
#     page_size = int(page_size)
#     offset = int(offset)
#
#     groups = Group.query.filter_by(teacher_id=teacher_id).all()
#     page_groups = groups[(offset-1) * page_size: offset * page_size]
#
#     total_pages = ceil(len(groups) / page_size)
#
#     data = groups2json(page_groups)
#     data['total_pages'] = total_pages
#
#     return jsonify(code=200, data=data)


# 获取邀请码
@group_bp.route('/invite_code/<group_id>', methods=['GET'])
def get_invite_code(group_id):
	group = Group.query.get(group_id)

	return jsonify(code=200, data={"group_id": group.id,
								   "invite_code": group.invite_code})

