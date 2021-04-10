# -*- coding: utf-8 -*- 
# @Time : 2021/4/6 20:09
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : __init__.py 
# @Software: PyCharm


import os

from flask import Flask
from flask_cors import CORS
from flask_login import current_user
from server.blueprints.auth import auth_bp
from server.blueprints.admin import admin_bp
from server.blueprints.home import home_bp
from server.extensions import db, mail, moment, login_manager
from server.models import User


def create_app(config_name=None):
    # if config_name is None:
    #     config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('server')
    CORS(app, supports_credentials=True)
    # cors = CORS(app, resources={r"/*": {"origins": "*"}})
    app.config.from_pyfile('settings.py')

    register_logging(app)  # 注册日志处理器
    register_extensions(app)  # 注册拓展
    register_blueprints(app)  # 注册蓝本
    regitser_shell_context(app)  # 注册shell上下文处理函数
    return app


def register_logging(app):
    pass


def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    moment.init_app(app)


def register_blueprints(app):
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(home_bp, url_prefix='/home')


def regitser_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db)

