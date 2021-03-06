# -*- coding: utf-8 -*- 
# @Time : 2021/4/6 18:10
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : emails.py 
# @Software:


from threading import Thread

from flask import current_app, render_template
from flask_mail import Message

from server.extensions import mail


def _send_async_mail(app, message):
    with app.app_context():
        mail.send(message)


def send_mail(to, subject, template, **kwargs):
    message = Message(current_app.config['SCRATCHAI_MAIL_SUBJECT_PREFIX'] + subject, recipients=[to])
    message.body = render_template(template + '.txt', **kwargs)
    app = current_app._get_current_object()
    thr = Thread(target=_send_async_mail, args=[app, message])
    thr.start()
    return thr


def send_confirm_email(user, url, to=None):
    send_mail(subject='Email Confirm', to=to or user.email, template='emails/confirm', user=user, url=url)


def send_reset_password_email(user, url):
    send_mail(subject='Password Reset', to=user.email, template='emails/reset_password', user=user, url=url)


def send_change_email_email(user, url, to=None):
    send_mail(subject='Change Email Confirm', to=to or user.email, template='emails/change_email', user=user, url=url)