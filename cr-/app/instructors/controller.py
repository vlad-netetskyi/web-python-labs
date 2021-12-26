from flask import url_for, render_template, redirect, \
    flash, abort, current_app
from flask_login import login_required
from .models import Teacher, Position
from .. import db, App
from flask_login import login_user, current_user, logout_user, login_required
import os
import secrets
from .forms import PostForm

from . import instructors_blueprint
from PIL import Image


@instructors_blueprint.route('/')
def index():
    teachers = Teacher.query.order_by(Teacher.start_work.desc())
    return render_template('teachers.html', teachers=teachers, menu=App.getMenu())


@instructors_blueprint.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = PostForm()
    positions = Position.query.all()

    form.position.choices = [(position.id, position.name) for position in positions]

    if form.validate_on_submit():
        teacher = Teacher(first_name=form.first_name.data,
                          last_name=form.last_name.data,
                          surname=form.surname.data,
                          position_id=form.position.data,
                          start_work=form.start_work.data,
                          chair=form.chair.data,
                          number_phone=form.number_phone.data
                          )

        db.session.add(teacher)
        db.session.commit()

        return redirect(url_for('teacher.index'))

    return render_template('create.html', form=form, menu=App.getMenu())


@instructors_blueprint.route('/<postId>', methods=['GET', 'POST'])
def view(postId):
    teacher = Teacher.query.get_or_404(postId)
    return render_template('teacher.html', teacher=teacher, menu=App.getMenu())


@instructors_blueprint.route('/<postId>/update', methods=['GET', 'POST'])
def update_post(postId):
    teacher = Teacher.query.get_or_404(postId)
    form = PostForm()

    positions = Position.query.all()

    form.position.choices = [(position.id, position.name) for position in positions]

    if form.validate_on_submit():

        teacher.first_name = form.first_name.data
        teacher.last_name = form.last_name.data
        teacher.surname = form.surname.data
        teacher.position_id = form.position.data
        teacher.start_work = form.start_work.data
        teacher.chair = form.chair.data
        teacher.number_phone = form.number_phone.data

        db.session.commit()

        flash('The post has been updated', category='success')
        return redirect(url_for('teacher.view', postId=teacher.id))

    form.first_name.data = teacher.first_name
    form.last_name.data = teacher.last_name
    form.surname.data = teacher.surname
    form.position.data = teacher.position_id
    form.start_work.data = teacher.start_work
    form.chair.data = teacher.chair
    form.number_phone.data = teacher.number_phone

    return render_template('create.html', form=form,
                           menu=App.getMenu())


@instructors_blueprint.route('/<postId>/delete', methods=['GET', 'POST'])
def delete_post(postId):
    teacher = Teacher.query.get_or_404(postId)
    db.session.delete(teacher)
    db.session.commit()

    return redirect(url_for('teacher.index', postId=postId))
'''

@instructors_blueprint.route('/<postId>/delete', methods=['GET', 'POST'])
def delete_post(postId):
    post = Post.query.get_or_404(postId)
    if current_user.id == post.user_id:
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('post.index'))

    flash('Post is not yours', category='warning')
    return redirect(url_for('post.view', postId=postId))




def get_category_name(id):
    return Category.query.get(id).name


current_app.jinja_env.globals.update(get_category_name=get_category_name)
'''
