# -*- coding: utf-8 -*- 
# @Time : 2021/4/7 17:49
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : user.py 
# @Software: PyCharm


from flask import current_app, jsonify, Blueprint
from flask_login import login_required, current_user

from server.emails import send_change_email_email
from server.extensions import db
from server.forms.user import EditUserForm
from server.models import User
from server.settings import Operations
from server.utils import generate_token, validate_token

user_bp = Blueprint('user', __name__)


@user_bp.route('/account/name', methods=['GET', 'POST'])
@login_required
def edit_name():
    form = EditUserForm()

    current_user.name = form.name.data
    db.session.commit()

    form.name.data = current_user.name
    return jsonify(code=400, data=form)