#!flask/bin/python
from flask import render_template, flash, request, redirect, make_response, jsonify

from flask import Flask, url_for
from DbHandler import DBHandler

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

import sys


db_handler = DBHandler()
app = Flask(__name__)
app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))
userLogged = dict()
cert = '/etc/letsencrypt/live/data4help.cloud/fullchain.pem'
key = '/etc/letsencrypt/live/data4help.cloud/privkey.pem'


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    email = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    company_name = StringField('Company Name', validators=[DataRequired()])
    submit = SubmitField('Sign Up')


def auth_user(cookie):
    email = cookie.get('email')
    if email:
        if cookie.get('password') == db_handler.get_third_party_password(email):
            return True
        else:
            return False


def set_cookies(user, psw):
    user_logged = {'username': user}
    res = make_response(render_template('private.html', title='OKKKKKK', user=user_logged, secret=get_secret(user)))
    res.set_cookie('email', user)
    res.set_cookie('password', psw)
    print("cookie settato")
    return res


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.password.data == db_handler.get_third_party_password(form.username.data):
            return set_cookies(form.username.data, form.password.data)

        return render_template('login.html', title='OKKK', form=form)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        db_handler.register_third_party(form.email.data, form.password.data,  form.company_name.data)
        flash('Signup requested for user {}'.format(form.email.data))
        return redirect(url_for('index'))
    return render_template('signup.html', title='Sign Up', form=form)


@app.route('/private_page',  methods=['GET', 'POST'])
def private_page():
    if auth_user(request.cookies):
        user_logged = {'username': request.cookies.get('email')}
        return render_template('private.html', title='OKKKKKK', user=user_logged, secret=get_secret())
    else:
        form = LoginForm()
        return redirect(url_for('login'))


@app.route('/log_out',  methods=['GET', 'POST'])
def log_out():
    res = make_response(render_template('index.html', title='Logged out'))
    res.set_cookie('email', '', expires=0)
    res.set_cookie('password', '', expires=0)
    return res


@app.route('/api/thirdparties/renew_third_party_secret', methods=['GET'])
def renew_third_party_secret():
    username = request.args.get('username')
    secret = request.args.get('secret')
    try:
        result = db_handler.check_third_party(username, secret)
        if result == 0:
            return jsonify({'Response': -1, 'Reason': 'Third-party not found'})
        else:
            try:
                db_handler.renew_third_party_secret(username)

            except Exception as e:
                print(str(e))
                return jsonify({'Response': -2, 'Reason': str(e)})
            user_logged = {'username': username}

            return render_template('private.html', title='OKKKKKK', user=user_logged, secret=get_secret())

    except Exception as e:
        print(str(e))
        return jsonify({'Response': -3, 'Reason': str(e)})


def get_secret(user=''):
    if user != '':
        return db_handler.get_third_party_secret(user)
    return db_handler.get_third_party_secret(request.cookies.get('email'))


if __name__ == '__main__':
    try:
        try:
            # try to run the WebAPP with SSL certificate active
            # context = (cert, key)
            app.run(host='0.0.0.0', port=443, ssl_context=context, threaded=True, debug=True)
        except :
            # old mode without SSL certificate for debugging in localhost
            app.run(host='0.0.0.0', port=80,threaded=True, debug=True)

    except KeyboardInterrupt:
        print("[*] Server shutted down")
        db_handler.db.close()
        sys.exit(0)
