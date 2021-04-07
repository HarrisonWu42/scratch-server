# -*- coding: utf-8 -*- 
# @Time : 2021/4/6 18:10
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : extensions.py 
# @Software: PyCharm


from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_moment import Moment

db = SQLAlchemy()
mail = Mail()
moment = Moment()