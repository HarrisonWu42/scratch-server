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
        task_obj = {"id": task.id, "name": task.name, "answer_video_url": task.answer_video_url}
        json_array.append(task_obj)
    json_dic = {"tasks": json_array}

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