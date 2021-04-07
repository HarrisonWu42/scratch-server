# -*- coding: utf-8 -*- 
# @Time : 2021/4/6 20:44
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : auth.py 
# @Software: PyCharm


from flask import flash, redirect, url_for, Blueprint, make_response, jsonify
from flask_login import login_user, logout_user, login_required, current_user, login_fresh, confirm_login
from server.emails import send_confirm_email, send_reset_password_email
from server.extensions import db
from server.forms.auth import RegisterForm, LoginForm
from server.models import User
from server.utils import generate_token

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is not None and user.validate_password(form.password.data):
            if login_user(user, form.remember_me.data):
                flash('Login success.', 'info')
                return jsonify(message='success')
            else:
                flash('Your account is blocked.', 'warning')
                # return redirect(url_for('main.index'))
        flash('Invalid email or password.', 'warning')
    # return render_template('auth/login.html', form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    # if current_user.is_authenticated:
    #     return redirect(url_for('main.index'))

    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data.lower()
        password = form.password.data
        user = User(name=name, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        token = generate_token(user=user, operation='confirm')
        send_confirm_email(user=user, token=token)
        flash('Confirm email sent, check your inbox.', 'info')
        # return redirect(url_for('.login'))
    return jsonify(message='success')