# -*- coding: utf-8 -*- 
# @Time : 2021/4/13 19:09
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : project.py 
# @Software: PyCharm


from flask import Blueprint, jsonify, request, make_response
from server.extensions import db
from server.models import User, Task, Project

project_bp = Blueprint('project', __name__)


@project_bp.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']


@project_bp.route('/download', methods=['GET'])
def download_file():
    file = request.files['file']