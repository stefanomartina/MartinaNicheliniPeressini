from flask import render_template, flash, request, redirect, make_response
from flask import Flask, url_for
from app import app
from app.forms import LoginForm, RegistrationForm
from app.dbHandler import DBHandler


db_handler = DBHandler()
res = ""
userLogged = dict()

def auth_user(cookie):
    db_handler.get_third_party_password(cookie.get('email'))
    if(cookie.get('password') == cookie.get('password')):
        return True

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print(form.password.data)
        print(db_handler.get_third_party_password(form.username.data))
        if(form.password.data == db_handler.get_third_party_password(form.username.data)):
            set_third_cookie(form.username.data, form.password.data)

        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        db_handler.register_third_party(form.email.data, form.password.data,  form.company_name.data)
        flash('Signup requested for user {}'.format(form.email.data))
        return redirect(url_for('index'))
    return render_template('signup.html', title='Sign Up', form=form)

def set_third_cookie(email, password):
    res = make_response("Setting a cookie")
    res.set_cookie('email', email)
    res.set_cookie('password', password)
    print("cookie settato")
    return res


@app.route('/private_page',  methods=['GET', 'POST'])
def private_page():
    if(auth_user(request.cookies)):
        render_template('index.html', title='OKKKKKK', user='ciao', posts={'author': {'username': 'John'},'body': 'Beautiful day in Portland!'})
    else:
        render_template('index.html', title='NOOOOOO', user='nooo', posts={'author': {'username': 'John'},'body': 'Beautiful day in Portland!'})
