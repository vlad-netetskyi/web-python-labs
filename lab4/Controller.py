from datetime import datetime
import os
from sys import version

from flask import render_template, request

from App import App

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, AnyOf

app = App().getApp()

REPORT_MESS = '<h1>The username is {}. The password is {}</h1>'
USERNAME_REQUIRED = 'A username is required!'
LENGTH_5_10 = 'length must be between 5 and 10 characters'


class LoginForm(FlaskForm):
    username = StringField('username',
                           validators=[InputRequired(USERNAME_REQUIRED),
                                       Length(min=5,
                                              max=10,
                                              message=LENGTH_5_10)])
    password = PasswordField('password',
                             validators=[InputRequired('password is require'),
                                         AnyOf(values=['password', 'secret'])])


@app.route('/form', methods=['GET', 'POST'])
def form():
    form = LoginForm()

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


if __name__ == '__main__':
    app.run(debug=True)
