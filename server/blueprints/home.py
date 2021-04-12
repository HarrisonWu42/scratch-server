# -*- coding: utf-8 -*- 
# @Time : 2021/4/7 11:38
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : home.py
# @Software: PyCharm


from flask import Blueprint, jsonify
from sqlalchemy import func
from server.extensions import db
from server.models import User, Task, Project

home_bp = Blueprint('home', __name__)


@home_bp.route('/', methods=['GET'])
def show_datas():
	# user_num = db.session.query(func.count(User.id)).first()
	user_num = User.query.count()
	# project_num = db.session.query(func.count(Project.id)).first()
	project_num = Project.query.count()
	# task_num = db.session.query(func.count(Task.id)).first()
	task_num = Task.query.count()
	return jsonify(code=200, data={"user_num": user_num,
								   "project_num": project_num,
								   "task_num": task_num})