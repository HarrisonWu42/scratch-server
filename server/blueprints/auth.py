# -*- coding: utf-8 -*- 
# @Time : 2021/4/6 20:44
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : auth.py 
# @Software: PyCharm


from flask import Blueprint

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login')
def login():
	pass


@auth_bp.route('/logout')
def logout():
	pass