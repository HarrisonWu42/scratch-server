# -*- coding: utf-8 -*- 
# @Time : 2021/4/6 20:44
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : admin.py 
# @Software: PyCharm


from flask import Blueprint, jsonify

from server.extensions import db
from server.forms.admin import EditRoleForm
from server.models import User, Role

admin_bp = Blueprint('admin', __name__)


# 查看所有用户的权限
@admin_bp.route('/users', methods=['GET'])
def users():
	users = User.query.all()

	json_array = []
	for user in users:
		user_obj = {"id": user.id,
					"name": user.name,
					"email": user.email,
					"role": user.role.name}
		json_array.append(user_obj)
	json_dic = {"users": json_array}

	return jsonify(code=200, data=json_dic)


# 查询所有权限
@admin_bp.route('/roles', methods=['GET'])
def roles():
	roles = Role.query.all()

	json_array = []
	for role in roles:
		role_obj = {"id": role.name,
					"name": role.email}
		json_array.append(role_obj)
	json_dic = {"roles": json_array}

	return jsonify(code=200, data=json_dic)


# 修改用户的权限
@admin_bp.route('/edit-role/<user_id>', methods=['POST'])
def edit_role(user_id):
	form = EditRoleForm()

	role = Role.query.filter_by(name=form.role.data).first()
	user = User.query.get(user_id)
	user.role_id = role.id
	db.session.commit()

	return jsonify(code=200, message="Edit success", data={"id": user.id,
														   "name": user.name,
														   "email": user.email,
														   "role": role.name})
