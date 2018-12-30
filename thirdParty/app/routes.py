from flask import render_template, flash, redirect
from flask import Flask, url_for
from app import app
from app.forms import LoginForm, RegistrationForm
from app.dbHandler import DBHandler

db_handler = DBHandler()

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
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
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