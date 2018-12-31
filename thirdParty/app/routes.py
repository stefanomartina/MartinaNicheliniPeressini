from flask import render_template, flash, request, redirect, make_response
from flask import Flask, url_for
from app import app
from app.forms import LoginForm, RegistrationForm
from app.dbHandler import DBHandler


db_handler = DBHandler()
userLogged = dict()


def auth_user(cookie):
    email = cookie.get('email')
    if(email):
        if(cookie.get('password') == db_handler.get_third_party_password(email)):
            return True
        else:
            return False


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if(form.password.data == db_handler.get_third_party_password(form.username.data)):
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
    if(auth_user(request.cookies)):
        user_logged = {'username' : request.cookies.get('email')}
        return render_template('private.html', title='OKKKKKK', user=user_logged)
    else:
        form = LoginForm()
        return render_template('login.html', title='Sign In', form=form)


@app.route('/log_out',  methods=['GET', 'POST'])
def log_out():
    res = make_response(render_template('index.html', title='Logged out'))
    res.set_cookie('email', '', expires=0)
    res.set_cookie('password', '', expires=0)
    return res


def set_cookies(user, psw):
    user_logged = {'username' : user}
    res = make_response(render_template('private.html', title='OKKKKKK', user=user_logged))
    res.set_cookie('email', user)
    res.set_cookie('password', psw)
    print("cookie settato")
    return res