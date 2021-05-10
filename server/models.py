# -*- coding: utf-8 -*- 
# @Time : 2021/4/6 18:09
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : models.py 
# @Software: PyCharm


import os
from datetime import datetime

from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from server.extensions import db

# relationship table
roles_permissions = db.Table('roles_permissions',
							 db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
							 db.Column('permission_id', db.Integer, db.ForeignKey('permission.id'))
							 )

users_groups = db.Table('users_groups',
						db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
						db.Column('group_id', db.Integer, db.ForeignKey('group.id'))
						)

groups_tasksets = db.Table('groups_tasksets',
						db.Column('group_id', db.Integer, db.ForeignKey('group.id')),
						db.Column('taskset_id', db.Integer, db.ForeignKey('taskset.id'))
						)

tasksets_tasks = db.Table('tasksets_tasks',
						db.Column('taskset_id', db.Integer, db.ForeignKey('taskset.id')),
						db.Column('task_id', db.Integer, db.ForeignKey('task.id'))
						)


class Permission(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(30), unique=True)
	roles = db.relationship('Role', secondary=roles_permissions, back_populates='permissions')


class Role(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(30), unique=True)

	users = db.relationship('User', back_populates='role')
	permissions = db.relationship('Permission', secondary=roles_permissions, back_populates='roles')

	@staticmethod
	def init_role():
		roles_permissions_map = {
			'Student': ['INVITED', 'PROJECT'],
			'Teacher': ['EVALUATE', 'TASK', 'GROUP', ],
			'Administrator': ['INVITED', 'PROJECT', 'EVALUATE', 'TASK', 'GROUP', 'ADMINISTER']
		}

		for role_name in roles_permissions_map:
			role = Role.query.filter_by(name=role_name).first()
			if role is None:
				role = Role(name=role_name)
				db.session.add(role)
			role.permissions = []
			for permission_name in roles_permissions_map[role_name]:
				permission = Permission.query.filter_by(name=permission_name).first()
				if permission is None:
					permission = Permission(name=permission_name)
					db.session.add(permission)
				role.permissions.append(permission)
		db.session.commit()


class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20))
	email = db.Column(db.String(254), unique=True, index=True)
	password_hash = db.Column(db.String(128))

	confirmed = db.Column(db.Boolean, default=False)

	role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
	role = db.relationship('Role', back_populates='users')

	projects = db.relationship('Project', back_populates='user')
	groups = db.relationship('Group', secondary=users_groups, back_populates='users')

	def __init__(self, **kwargs):
		super(User, self).__init__(**kwargs)
		self.set_role()

	def get_id(self):
		return self.id

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def set_role(self):
		if self.role is None:
			if self.email == current_app.config['ADMIN_EMAIL']:
				self.role = Role.query.filter_by(name='Administrator').first()
			elif self.email.split('@')[-1] == current_app.config['TEACHER_EMAIL']:
				self.role = Role.query.filter_by(name='Teacher').first()
			else:
				self.role = Role.query.filter_by(name='Student').first()
			db.session.commit()

	def validate_password(self, password):
		return check_password_hash(self.password_hash, password)

	@property
	def is_admin(self):
		return self.role.name == 'Administrator'

	@property
	def is_teacher(self):
		return self.role.name == 'Teacher'


class Group(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), unique=True, index=True)
	description = db.Column(db.String(80))
	type = db.Column(db.Integer, index=True)  # type=0: 关闭组 type=1: 开放组
	teacher_id = db.Column(db.Integer, index=True)

	invite_code = db.Column(db.String(6), unique=True)

	users = db.relationship('User', secondary=users_groups, back_populates='groups')
	tasksets = db.relationship('Taskset', secondary=groups_tasksets, back_populates='groups')


class Project(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(30))
	score = db.Column(db.Integer)
	comment = db.Column(db.Text)
	correct_timestamp = db.Column(db.DateTime)
	commit_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
	logicality = db.Column(db.Float)
	workload = db.Column(db.Float)
	complexity = db.Column(db.Float)
	deleted = db.Column(db.Integer, default=0)

	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	user = db.relationship('User', back_populates='projects')

	teacher_id = db.Column(db.Integer)

	task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
	task = db.relationship('Task', back_populates='projects')


class Task(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(30), unique=True)
	description = db.Column(db.String(80))
	commit_num = db.Column(db.Integer, default=0)
	perfect_num = db.Column(db.Integer, default=0)
	answer_video_url = db.Column(db.String(120))

	projects = db.relationship('Project', back_populates='task')
	tasksets = db.relationship('Taskset', secondary=tasksets_tasks, back_populates='tasks')


class Taskset(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(30), unique=True)
	type = db.Column(db.Integer)  # type=0: 非固定任务集 type=1:固定任务集

	tasks = db.relationship('Task', secondary=tasksets_tasks, back_populates='tasksets')
	groups = db.relationship('Group', secondary=groups_tasksets, back_populates='tasksets')