# -*- coding: utf-8 -*- 
# @Time : 2021/4/6 18:10
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : utils.py 
# @Software: PyCharm


import os
import uuid

try:
    from urlparse import urlparse, urljoin
except ImportError:
    from urllib.parse import urlparse, urljoin

from flask import current_app, request, url_for, redirect, flash
from itsdangerous import BadSignature, SignatureExpired
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from server.settings import Operations
from server.extensions import db
from server.models import User


def generate_token(user, operation, expire_in=None, **kwargs):
    s = Serializer(current_app.config['SECRET_KEY'], expire_in)

    data = {'id': user.id, 'operation': operation}
    data.update(**kwargs)
    return s.dumps(data)


def validate_token(user, token, operation, new_password=None):
    s = Serializer(current_app.config['SECRET_KEY'])

    try:
        data = s.loads(token)
    except (SignatureExpired, BadSignature):
        return False

    if operation != data.get('operation') or user.id != data.get('id'):
        return False

    if operation == Operations.CONFIRM:
        user.confirmed = True
    elif operation == Operations.RESET_PASSWORD:
        user.set_password(new_password)
    elif operation == Operations.CHANGE_EMAIL:
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if User.query.filter_by(email=new_email).first() is not None:
            return False
        user.email = new_email
    else:
        return False

    db.session.commit()
    return True


def extract_id_from_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])

    try:
        data = s.loads(token)
    except (SignatureExpired, BadSignature):
        return False

    id = data.get('id')

    return id


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def tasks2json(tasks):

    json_array = []
    for task in tasks:
        if task.commit_num > 0:
            perfect_rate = round(task.perfect_num / task.commit_num, 2)
        else:
            perfect_rate = None

        task_obj = {"id": task.id,
                    "name": task.name,
                    "description": task.description,
                    "commit_num": task.commit_num,
                    "perfect_num": task.perfect_num,
                    "perfect_rate": perfect_rate,
                    "answer_video_url": task.answer_video_url}
        json_array.append(task_obj)
    json_dic = {"tasks": json_array}

    return json_dic


def taskset2json(tasksets):

    json_array = []
    for taskset in tasksets:
        if taskset.type == 1:
            taskset_type = "固定任务集"
        else:
            taskset_type = "私有任务集"
        taskset_obj = {"id": taskset.id,
                    "name": taskset.name,
                    "type": taskset_type}
        json_array.append(taskset_obj)
    json_dic = {"tasksets": json_array}

    return json_dic


def groups2json(groups):

    json_array = []
    for group in groups:
        group_obj = {"id": group.id,
                     "name": group.name,
                     "description": group.description,
                     "type": group.type,
                     "teacher_id": group.teacher_id,
                     "invite_code": group.invite_code}
        json_array.append(group_obj)
    json_dic = {"groups": json_array}

    return json_dic


def users2json(users):

    json_array = []
    for user in users:
        user_obj = {"id": user.id,
                     "name": user.name,
                     "email": user.email}
        json_array.append(user_obj)
    json_dic = {"students": json_array}

    return json_dic


def bprojects2json(projects):
    json_array = []
    for project in projects:
        project_obj = {"id": project.id,
                       "name": project.name,
                       "commit_timestamp": project.commit_timestamp}
        json_array.append(project_obj)
    json_dic = {"projects": json_array}

    return json_dic


def xlsx_style(**kwargs):
    style = {
        'bold': kwargs.get('bold', False),  # 加粗
        'font_name': kwargs.get('font_name', 'SimSun'),  # 字体类型，默认宋体
        'font_size': kwargs.get('font_size', 12),  # 字体大小，默认12
        'font_color': kwargs.get('font_color', '#000000'),  # 字体颜色，黑色
        'align': kwargs.get('align', 'center'),  # 默认水平居中
        'valign': kwargs.get('valign', 'vcenter'),  # 默认垂直居中
        'text_wrap': kwargs.get('text_wrap', True),  # 默认自动换行
        'top': kwargs.get('top', 1),  # 上边界，线条宽度
        'bottom': kwargs.get('bottom', 1),  # 边界
        'left': kwargs.get('left', 1),  # 边界
        'right': kwargs.get('right', 1),  # 边界
        'bg_color': kwargs.get('bg_color', '#FFFFFF'),  # 背景颜色，白色
        # 其他类型设置格式可以接着写
    }

    return style