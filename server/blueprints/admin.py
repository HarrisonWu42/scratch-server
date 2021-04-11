# -*- coding: utf-8 -*- 
# @Time : 2021/4/6 20:44
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : admin.py 
# @Software: PyCharm


from flask import Blueprint


admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/emails')
def index():

	pass