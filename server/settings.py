# -*- coding: utf-8 -*- 
# @Time : 2021/4/6 19:27
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : settings.py 
# @Software: PyCharm


import os
import sys


basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class Operations:
    CONFIRM = 'confirm'
    RESET_PASSWORD = 'reset-password'
    CHANGE_EMAIL = 'change-email'


# 'mysql+pymysql://用户名称:密码@localhost:端口/数据库名称'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost:3306/testdb'
SQLALCHEMY_TRACK_MODIFICATIONS = True


SECRET_KEY = os.getenv('SECRET_KEY', 'secret string')
