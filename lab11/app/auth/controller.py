from flask import url_for, render_template, flash, redirect, abort
from .. import db, App, bcrypt
from .forms import RegistrationForm, LoginForm
from .models import User
from flask_login import login_user, current_user, logout_user, login_required

from . import auth_blueprint


@auth_blueprint.route('/')
def index():
    return 'Good'


@auth_blueprint.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('You are already loggined in', category='warning')
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data,
                        email=form.email.data,
                        password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash(f'Account created for {form.username.data} !',
              category='success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form, menu=App.getMenu())


@auth_blueprint.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first()
            email = user.email
        except AttributeError:
            flash('Invalid login!', category='warning')
            return redirect(url_for('auth.login'))

        if form.email.data == email and user.verify_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'Logged in by username {user.username}!', category='success')
            return redirect(url_for('about'))
        else:
            flash('Login unsuccessful', category='warning')

    return render_template('auth/login.html', form=form, menu=App.getMenu())


@auth_blueprint.route("/users", methods=['GET', 'POST'])
@login_required
def users():
    all_users = User.query.all()
    count = User.query.count()
    if count == 0:
        abort(404)

    return render_template('auth/users.html',
                           all_users=all_users,
                           count=count,
                           menu=App.getMenu())


@auth_blueprint.route("/logout")
def logout():
    logout_user()
    flash('You have been logged out!')
    return redirect(url_for('index'))


@auth_blueprint.route("/account")
@login_required
def account():
    return render_template('auth/account.html', user=current_user, menu=App.getMenu())