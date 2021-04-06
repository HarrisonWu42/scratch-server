# -*- coding: utf-8 -*- 
# @Time : 2021/4/6 20:09
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : __init__.py 
# @Software: PyCharm
import os

from flask import Flask

from server.blueprints.auth import auth_bp
from server.blueprints.admin import admin_bp
from server.extensions import db, mail, moment


def create_app(config_name=None):
    # if config_name is None:
    #     config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('server')
    app.config.from_pyfile('settings.py')

    register_logging(app)  # 注册日志处理器
    register_extensions(app)  # 注册拓展
    register_blueprints(app)  # 注册蓝本

    return app


def register_logging(app):
    pass


def register_extensions(app):
    db.init_app(app)
    mail.init_app(app)
    moment.init_app(app)


def register_blueprints(app):
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')