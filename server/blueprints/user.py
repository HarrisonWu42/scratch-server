# -*- coding: utf-8 -*- 
# @Time : 2021/4/7 17:49
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : user.py 
# @Software: PyCharm


from flask import render_template, flash, redirect, url_for, current_app, jsonify, Blueprint
from flask_login import login_required, current_user, fresh_login_required, logout_user

from server.emails import send_change_email_email
from server.extensions import db
from server.forms.user import EditNameForm, ChangeEmailForm, ChangePasswordForm
from server.models import User
from server.settings import Operations
from server.utils import generate_token, validate_token, redirect_back

user_bp = Blueprint('user', __name__)


@user_bp.route('/account/name', methods=['GET', 'POST'])
@login_required
def edit_name():
    form = EditNameForm()

    current_user.name = form.name.data
    db.session.commit()

    form.name.data = current_user.name
    return jsonify(code=400, data=form)