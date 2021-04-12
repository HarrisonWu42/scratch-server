# -*- coding: utf-8 -*- 
# @Time : 2021/4/7 18:26
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : group.py 
# @Software: PyCharm


import random
from flask import Blueprint, jsonify, request
from flask_paginate import Pagination, get_page_parameter

from server.extensions import db
from server.forms.group import GroupForm, EditGroupForm, CloseGroupForm, DeleteGroupForm, InviteGroupForm
from server.models import Group, User
from server.utils import groups2json, users2json

group_bp = Blueprint('group', __name__)


# 显示某个老师的班组
@group_bp.route('/teacher/<id>/<offset>/<per_page>', methods=['GET'])
def show_tasks(id, offset, per_page):
	id = int(id)
	per_page = int(per_page)
	offset = int(offset)

	groups = Group.query.filter_by(teacher_id=id).limit(per_page).offset((offset-1) * per_page)
	data = groups2json(groups)

	return jsonify(code=200, data=data)


# !!!!这个有问题的， group还缺删除某个班组的某个学生
# 显示某个班组的所有学生
@group_bp.route('/<id>/<offset>/<per_page>', methods=['GET'])
def show_students(id, offset, per_page):
	id = int(id)
	per_page = int(per_page)
	offset = int(offset)

	group = Group.query.get(id)
	users = group.users.limit(per_page).offset((offset - 1) * per_page)
	users_paginate = users.paginate(per_page=10)

	data = users2json(users)

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

	group = Group(name=name, description=description, type=True, teacher_id=teacher_id, invite_code=invite_code)

	db.session.add(group)
	db.session.commit()

	group = Group.query.filter_by(name=name).first()

	return jsonify(code=200, message="Add task success.", data={"id": group.id,
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

	return jsonify(code=200, message="Add task success.", data={"id": group.id,
																"name": group.name,
																"description": group.description,
																"type": group.type,
																"teacher_id": group.teacher_id,
																"invite_code": group.invite_code})


# 关闭班组
@group_bp.route('/close', methods=['POST'])
def close():
	form = CloseGroupForm()

	id = form.id.data

	group = Group.query.get(id)

	group.type = False

	db.session.commit()

	return jsonify(code=200, message="Add task success.", data={"id": group.id,
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

	return jsonify(code=200, message="Delete success", data={"id": group.id,
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
