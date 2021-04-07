# -*- coding: utf-8 -*- 
# @Time : 2021/4/6 18:09
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : models.py 
# @Software: PyCharm


import os
from datetime import datetime

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


class Permission(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(30), unique=True)
	roles = db.relationship('Role', secondary=roles_permissions, back_populates='permissions')


class Role(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(30), unique=True)

	users = db.relationship('User', back_populates='role')
	permissions = db.relationship('Permission', secondary=roles_permissions, back_populates='roles')


class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20))
	email = db.Column(db.String(254), unique=True, index=True)
	password_hash = db.Column(db.String(128))

	role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
	role = db.relationship('Role', back_populates='users')

	projects = db.relationship('Project', back_populates='user')
	groups = db.relationship('Group', secondary=users_groups, back_populates='users')


class Group(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, index=True)
	description = db.Column(db.String(80))
	type = db.Column(db.String(5), unique=True, index=True)
	teacher_id = db.Column(db.Integer, index=True)

	users = db.relationship('User', secondary=users_groups, back_populates='groups')


class Project(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(30), unique=True)
	score = db.Column(db.Integer)
	comment = db.Column(db.Text)
	correct_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
	commit_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
	logicality = db.Column(db.Float)
	workload = db.Column(db.Float)
	complexity = db.Column(db.Float)

	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	user = db.relationship('User', back_populates='projects')

	teacher_id = db.Column(db.Integer)

	task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
	task = db.relationship('Task', back_populates='projects')


class Task(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(30), unique=True)
	projects = db.relationship('Project', back_populates='task')
