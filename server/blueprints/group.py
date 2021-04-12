# -*- coding: utf-8 -*- 
# @Time : 2021/4/7 18:26
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : group.py 
# @Software: PyCharm


import random
from math import ceil

from flask import Blueprint, jsonify, request

from server.extensions import db
from server.forms.group import GroupForm, EditGroupForm, CloseGroupForm, DeleteGroupForm, InviteGroupForm, KickGroupForm
from server.models import Group, User
from server.utils import groups2json, users2json

group_bp = Blueprint('group', __name__)


# 显示某个老师的班组
@group_bp.route('/teacher/<teacher_id>/<offset>/<page_size>', methods=['GET'])
def show_tasks(teacher_id, offset, page_size):
	teacher_id = int(teacher_id)
	page_size = int(page_size)
	offset = int(offset)

	groups = Group.query.filter_by(teacher_id=teacher_id).all()
	page_groups = groups[(offset-1) * page_size: offset * page_size]

	total_pages = ceil(len(groups) / page_size)

	data = groups2json(page_groups)
	data['total_pages'] = total_pages

	return jsonify(code=200, data=data)


# 显示某个班组的所有学生
@group_bp.route('/<group_id>/<offset>/<page_size>', methods=['GET'])
def show_students(group_id, offset, page_size):
	id = int(group_id)
	page_size = int(page_size)
	offset = int(offset)

	group = Group.query.get(id)
	users = group.users  # 所有users
	page_users = users[(offset-1) * page_size: offset * page_size]

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

	return jsonify(code=200, message="Add success.", data={"id": group.id,
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

	return jsonify(code=200, message="Edit success.", data={"id": group.id,
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

	return jsonify(code=200, message="Delete success.", data={"id": group.id,
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

	group.type = 0

	db.session.commit()

	return jsonify(code=200, message="Close success.", data={"id": group.id,
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