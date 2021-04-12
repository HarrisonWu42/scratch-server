# -*- coding: utf-8 -*- 
# @Time : 2021/4/7 17:49
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : user.py 
# @Software: PyCharm


from flask import current_app, jsonify, Blueprint, url_for
from flask_login import login_required, current_user

from server.emails import send_change_email_email
from server.extensions import db
from server.forms.user import EditNameForm, ChangeEmailForm
from server.utils import generate_token

user_bp = Blueprint('user', __name__)


# 修改昵称
@user_bp.route('/edit-name', methods=['POST'])
@login_required
def edit_name():
    form = EditNameForm()

    current_user.name = form.name.data
    db.session.commit()

    form.name.data = current_user.name
    return jsonify(code=200, message="Edit success", data={"id": current_user.id,
                                                           "name": current_user.name,
                                                           "email": current_user.email})


# 修改邮箱(还没写好)
@user_bp.route('/change-email', methods=['POST'])
@login_required
def change_email():
    form = ChangeEmailForm()

    current_user.email = form.email.data
    db.session.commit()

    form.email.data = current_user.email

    # 发邮件
    token = generate_token(user=current_user, operation='confirm')
    url = "http://localhost:8080/#" + url_for(endpoint='user.change_email', token=token)
    send_change_email_email(user=current_user, url=url)

    current_user.confirmed = 0
    db.session.commit()

    return jsonify(code=200, message="Change email success", data={"id": current_user.id,
                                                                   "name": current_user.name,
                                                                   "email": current_user.email})
