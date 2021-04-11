# -*- coding: utf-8 -*- 
# @Time : 2021/4/7 17:57
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : task.py
# @Software: PyCharm
from flask import Blueprint

task_bp = Blueprint('auth', __name__)


# # 发布任务
# @task_bp.route('/test', methods=['POST', 'GET'])
# def test():
#     if current_user.is_authenticated():
#         print(2222)
#     print(11111111111111)
#
#
# # 修改任务
# @task_bp.route('/test', methods=['POST', 'GET'])
# def test():
#     if current_user.is_authenticated():
#         print(2222)
#     print(11111111111111)
#
#
# # 删除任务
# @task_bp.route('/test', methods=['POST', 'GET'])
# def test():
#     if current_user.is_authenticated():
#         print(2222)
#     print(11111111111111)
