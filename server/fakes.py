# -*- coding: utf-8 -*- 
# @Time : 2021/4/6 21:09
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : fakes.py 
# @Software: PyCharm


import random
from datetime import datetime

from faker import Faker
from sqlalchemy.exc import IntegrityError
from server.extensions import db
from server.models import User, Group, Project, Task, Taskset

fake = Faker()


def fake_db():
	fake_user(10)
	fake_group(3)
	fake_taskset(3)
	fake_task(10)

	fake_task2taskset()
	fake_user2group()
	fake_taskset2group()

	fake_project()


def fake_user(count=10):
	user = User(name="teacher", email=fake.email(), confirmed=True)
	user.set_password('123456')
	db.session.add(user)

	for i in range(count):
		user = User(name=fake.name(),
					email=fake.email(),
					confirmed=True)
		user.set_password('123456')
		db.session.add(user)
		try:
			db.session.commit()
		except IntegrityError:
			db.session.rollback()


def fake_group(count=5):
	for i in range(count):
		invite_code = "".join(item for item in random.sample('0123456789', 6))
		while Group.query.filter_by(invite_code=invite_code).first() is not None:
			invite_code = "".join(item for item in random.sample('0123456789', 6))

		group = Group(name=fake.name(),
					  description=fake.text(max_nb_chars=20),
					  type=1,
					  invite_code=invite_code,
					  teacher_id=1)

		db.session.add(group)
		try:
			db.session.commit()
		except IntegrityError:
			db.session.rollback()


def fake_taskset(count=3):
	for i in range(count):
		taskset = Taskset(name=fake.name(), type=0)

		db.session.add(taskset)
		try:
			db.session.commit()
		except IntegrityError:
			db.session.rollback()

	for i in range(count):
		taskset = Taskset(name=fake.name(), type=1)

		db.session.add(taskset)
		try:
			db.session.commit()
		except IntegrityError:
			db.session.rollback()


def fake_task(count=20):
	for i in range(count):
		task = Task(name=fake.name(),
					description=fake.text(max_nb_chars=20),
					answer_video_url="www.baidu.com")

		db.session.add(task)
		try:
			db.session.commit()
		except IntegrityError:
			db.session.rollback()


def fake_task2taskset():
	tasksets = Taskset.query.all()
	tasks = Task.query.all()
	for taskset in tasksets:
		for task in tasks:
			if random.randint(0, 1) == 1:
				taskset.tasks.append(task)
	try:
		db.session.commit()
	except IntegrityError:
		db.session.rollback()


def fake_user2group():
	users = User.query.all()
	groups = Group.query.all()
	for group in groups:
		for user in users:
			if random.randint(0, 1) == 1:
				group.users.append(user)
	try:
		db.session.commit()
	except IntegrityError:
		db.session.rollback()


def fake_taskset2group():
	groups = Group.query.all()
	tasksets = Taskset.query.all()
	for group in groups:
		for taskset in tasksets:
			if random.randint(0, 1) == 1:
				group.tasksets.append(taskset)
	try:
		db.session.commit()
	except IntegrityError:
		db.session.rollback()


def fake_project(count=100):
	users = User.query.filter(User.id != 1).all()

	for i in range(count):
		user = users[random.randint(0, len(users)-1)]
		groups = user.groups
		if len(groups) > 0:
			group = groups[random.randint(0, len(groups)-1)]
			tasksets = group.tasksets
			if len(tasksets) > 0:
				taskset  = tasksets[random.randint(0, len(tasksets)-1)]
				tasks = taskset.tasks
				if len(tasks)>0:
					task = tasks[random.randint(0, len(tasks)-1)]
					project = Project(name=fake.name(),
									  score=random.randint(1, 5),
									  comment=fake.text(max_nb_chars=20),
									  commit_timestamp=datetime.utcnow(),
									  logicality=random.random(),
									  workload=random.randint(1, 100),
									  complexity=random.randint(1, 100),
									  user_id=user.id,
									  teacher_id=1,
									  task_id=task.id)
					db.session.add(project)
		try:
			db.session.commit()
		except IntegrityError:
			db.session.rollback()