from datetime import datetime
import os
from sys import version

from flask import render_template, request, flash, session, redirect, url_for

from app.forms import LoginFormSecond, LoginForm, RegistrationForm
from app.file_writer import writeToFile
from app import app, App, db, bcrypt
from app.custom_validator import validate
from .models import User


@app.route('/form_second', methods=['GET', 'POST'])
def form_second():
    form = LoginFormSecond()
    validate(form=form)

    if form.validate_on_submit():
        writeToFile(form)
        flash('User has been written in json file')
        session['login'] = form.login.data
        session['e_l_number'] = form.e_l_number.data
        return render_template("result.html",
                               form=form,
                               menu=App.getMenu())

    return render_template("form_second.html",
                           login=session['login'],
                           e_l_number=session['e_l_number'],
                           form=form,
                           menu=App.getMenu())


@app.route('/form', methods=['GET', 'POST'])
def form():
    form = LoginForm()
    REPORT_MESS = '<h1>The username is {}. The password is {}</h1>'
    if form.validate_on_submit():
        return REPORT_MESS.format(form.username.data, form.password.data)
    return render_template("form.html",
                           form=form,
                           menu=App.getMenu(),
                           operating_system=os.name,
                           user_agent=request.user_agent,
                           python_version=version,
                           time=datetime.now().strftime("%H:%M:%S")
                           )


@app.route('/')
def index():
    return render_template("main.html", menu=App.getMenu(),
                           operating_system=os.name,
                           user_agent=request.user_agent,
                           python_version=version,
                           time=datetime.now().strftime("%H:%M:%S")
                           )


@app.route("/about")
def about():
    return render_template("about.html", menu=App.getMenu(),
                           operating_system=os.name,
                           user_agent=request.user_agent,
                           python_version=version,
                           time=datetime.now().strftime("%H:%M:%S"))


@app.route("/achievements")
def score():
    return render_template("achievements.html", menu=App.getMenu(),
                           operating_system=os.name,
                           user_agent=request.user_agent,
                           python_version=version,
                           time=datetime.now().strftime("%H:%M:%S"))


@app.route("/register", methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data,
                        email=form.email.data,
                        password=bcrypt.generate_password_hash(str(form.password.data)))
        db.session.add(new_user)
        db.session.commit()
        flash(f'Account created for {form.username.data} !',
              category='success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form, menu=App.getMenu())


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first()
            email = user.email
            password = user.password
        except AttributeError:
            flash('Invalid login!', category='warning')
            return redirect(url_for('login'))

        if form.email.data == email and bcrypt.check_password_hash(password, form.password.data):
            flash(f'Logged in by username {user.username}!', category='success')
            return redirect(url_for('about'))
        else:
            flash('Login unsuccessful', category='warning')

    return render_template('login.html', form=form, menu=App.getMenu())


@app.route("/users")
def users():
    all_users = User.query.all()
    count = User.query.count()

    return render_template('users.html',
                           all_users=all_users,
                           count=count,
                           menu=App.getMenu())
