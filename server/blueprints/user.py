# -*- coding: utf-8 -*- 
# @Time : 2021/4/7 17:49
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : user.py 
# @Software: PyCharm


from flask import current_app, jsonify, Blueprint, url_for
from flask_login import login_required, current_user

from server.models import User
from server.emails import send_change_email_email
from server.extensions import db
from server.forms.user import EditNameForm, ChangeEmailForm
from server.utils import generate_token

user_bp = Blueprint('user', __name__)


# 修改昵称
@user_bp.route('/edit-name/<user_id>', methods=['POST'])
# @login_required
def edit_name(user_id):
    form = EditNameForm()

    # current_user.name = form.name.data
    user = User.query.get(user_id)
    user.name = form.name.data
    db.session.commit()

    # form.name.data = current_user.name
    return jsonify(code=200, message="Edit success", data={"id": user.id,
                                                           "name": user.name,
                                                           "email": user.email})


# 修改邮箱(还没写好)
@user_bp.route('/change-email/<user_id>', methods=['POST'])
# @login_required
def change_email(user_id):
    form = ChangeEmailForm()

    # current_user.email = form.email.data
    user = User.query.get(user_id)
    user.email = form.email.data
    user.confirmed = 0
    db.session.commit()

    # form.email.data = current_user.email

    # 发邮件
    token = generate_token(user=user, operation='confirm')
    url = "http://localhost:8080/#" + url_for(endpoint='user.change_email', token=token)
    send_change_email_email(user=user, url=url)

    return jsonify(code=200, message="Change email success", data={"id": user.id,
                                                                   "name": user.name,
                                                                   "email": user.email})
