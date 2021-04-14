# -*- coding: utf-8 -*- 
# @Time : 2021/4/7 17:49
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : user.py 
# @Software: PyCharm


from flask import current_app, jsonify, Blueprint, url_for

from server.models import User
from server.emails import send_change_email_email
from server.extensions import db
from server.forms.user import EditNameForm, ChangeEmailForm
from server.settings import Operations
from server.utils import generate_token, extract_id_from_token, validate_token

user_bp = Blueprint('user', __name__)


# 修改昵称
@user_bp.route('/edit-name/<user_id>', methods=['POST'])
def edit_name(user_id):
    form = EditNameForm()

    user = User.query.get(user_id)
    user.name = form.name.data
    db.session.commit()

    return jsonify(code=200, message="Edit success", data={"id": user.id,
                                                           "name": user.name,
                                                           "email": user.email})


# 修改邮箱
@user_bp.route('/change-email/<user_id>', methods=['POST'])
def change_email(user_id):
    form = ChangeEmailForm()

    # current_user.email = form.email.data
    user = User.query.get(user_id)
    user.email = form.email.data
    user.confirmed = 0
    db.session.commit()

    # 发邮件
    token = generate_token(user=user, operation=Operations.CHANGE_EMAIL)
    url = "http://localhost:8080/#" + url_for(endpoint='user.confirm_change_email', token=token)
    send_change_email_email(user=user, url=url)

    return jsonify(code=200, message="Change email success", data={"id": user.id,
                                                                   "name": user.name,
                                                                   "email": user.email})


# 修改邮箱确认
@user_bp.route('/confirm_change_email/<token>', methods=['POST'])
def confirm_change_email(token):
    user_id = extract_id_from_token(token)
    user = User.query.get(user_id)

    if user.confirmed:
        return jsonify(code=303, message="Redirect to main page.")

    if validate_token(user=user, token=token, operation=Operations.CHANGE_EMAIL):
        return jsonify(code=200, message="Confirm success.")
    else:
        return jsonify(code=400, message="Error, invalid or expired token.")

