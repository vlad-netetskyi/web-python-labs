import os
import secrets
from PIL import Image

from flask import url_for, render_template, flash, redirect,\
    abort, request, current_app
from .. import db, App
from .forms import RegistrationForm, LoginForm, UpdateAccountForm
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


@auth_blueprint.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated", category="success")
        return redirect(url_for('auth.account'))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image = url_for('static',
                    filename='profile_pics/' + current_user.image_file)
    return render_template('auth/account.html',
                           user=current_user,
                           menu=App.getMenu(),
                           image=image,
                           form=form)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path,
                                'static\\profile_pics', picture_fn)
    output_size = (200, 200)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn
