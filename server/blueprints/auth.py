# -*- coding: utf-8 -*- 
# @Time : 2021/4/6 20:44
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : auth.py 
# @Software: PyCharm


from flask import flash, redirect, url_for, Blueprint, make_response, jsonify
from flask_cors import CORS
from flask_login import login_user, logout_user, login_required, current_user, login_fresh, confirm_login
from server.emails import send_confirm_email, send_reset_password_email
from server.extensions import db
from server.forms.auth import RegisterForm, LoginForm
from server.models import User
from server.settings import Operations
from server.utils import generate_token, validate_token, redirect_back

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:  # 是否登录
        return jsonify(code=302, message="redirect to main page.")

    form = LoginForm()

    user = User.query.filter_by(email=form.email.data.lower()).first()
    if user is not None and user.validate_password(form.password.data):
        if login_user(user):
            return jsonify(code=200, message='success')
        else:
            return jsonify(code=400, message='Your account is blocked, warning!')

    return jsonify(code=400, message='Invalid emails or password, warning!')


# @auth_bp.route('/re-authenticate', methods=['GET', 'POST'])
# @login_required
# def re_authenticate():
#     if login_fresh():
#         return redirect(url_for('main.index'))
#
#     form = LoginForm()
#     if form.validate_on_submit() and current_user.validate_password(form.password.data):
#         confirm_login()
#         return redirect_back()
#     # return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout success.', 'info')
    return redirect(url_for('main.index'))


@auth_bp.route('/register', methods=['POST'])
def register():
    # if current_user.is_authenticated:
    #     return jsonify(code=302, message="redirect to main page.")

    form = RegisterForm()

    user = User.query.filter_by(email=form.email.data.lower()).first()
    if user is not None:
        return jsonify(code=302, message="user already exist.")

    name = form.name.data
    email = form.email.data.lower()
    password = form.password.data
    user = User(name=name, email=email)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    user = User.query.filter_by(email=form.email.data.lower()).first()
    id = user.id

    token = generate_token(user=user, operation='confirm')

    send_confirm_email(user=user, token=token)
    # flash('Confirm emails sent, check your inbox.', 'info')
    return jsonify(code=303, message="redirect to login page.", data={"id": id})


@auth_bp.route('/confirm/<token>')
def confirm(token):
    if current_user.confirmed:
        return jsonify(code=204, message="Account confirmed.")

    if validate_token(user=current_user, token=token, operation=Operations.CONFIRM):
        return jsonify(code=200, message="Account confirmed, success")
    else:
        return jsonify(code=400, message="Invalid or expired token, fail")