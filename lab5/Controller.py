from datetime import datetime
import os
from sys import version

from flask import render_template, request

from App import App

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import InputRequired, Length, AnyOf, Regexp, EqualTo

import json

app = App().getApp()

REPORT_MESS = '<h1>The username is {}. The password is {}</h1>'
REQUIRED = 'A {} is required!'
LENGTH_BETWEEN = 'length must be between {} and {} characters'
LENGTH_MIN = 'length must be at least {} characters'
LENGTH = 'length must be {} characters'
REGEXP = 'input must be for regex ({})'
PASSWORD = 'passwords must match'


class LoginForm(FlaskForm):
    username = StringField('username',
                           validators=[InputRequired(REQUIRED.format('username')),
                                       Length(min=5, max=10,
                                              message=LENGTH_BETWEEN.format(5, 10))])
    password = PasswordField('password',
                             validators=[InputRequired(REQUIRED.format('password')),
                                         AnyOf(values=['password', 'qwerty'])])


class LoginFormSecond(FlaskForm):
    login = StringField('Login(email address) *',
                        validators=[InputRequired(REQUIRED.format('login'))])

    password = PasswordField('Password *',
                             validators=[InputRequired(REQUIRED.format('password')),
                                         Length(min=6, message=LENGTH_MIN.format(6))])

    password_confirm = PasswordField('Password confirmation *',
                                     validators=[InputRequired(REQUIRED.format('password')),
                                                 Length(min=6, message=LENGTH_MIN.format(6)),
                                                 EqualTo('password', message=PASSWORD)])

    e_l_number = StringField('Number *', validators=[InputRequired(REQUIRED.format('number')),
                                                     Length(min=7, max=7,
                                                            message=LENGTH.format(7)),
                                                     Regexp(regex='^[0-9]+$',
                                                            message=REGEXP.format('^[0-9]+$'))])

    e_l_pin = PasswordField('PIN *', validators=[InputRequired(REQUIRED.format('PIN')),
                                                 Length(min=4, max=4, message=LENGTH.format(4)),
                                                 Regexp(regex='^[0-9]+$', message=REGEXP.format('^[0-9]+$'))])

    e_l_year = SelectField('Year *', choices=[2014, 2015, 2016, 2017,
                                              2018, 2019, 2020, 2021])
    d_f_e_series = StringField('Serion')
    d_f_e_number = StringField('Number *')


def writeToFile(form: LoginFormSecond):
    login = form.login.data
    data = {
        "login": login,
        "password": form.password.data,
        "Examenation list number": form.e_l_number.data,
        "Examenation list PIN": form.e_l_pin.data,
        "Examenation list year": form.e_l_year.data,
        "Document education series": form.d_f_e_series.data,
        "Document education number": form.d_f_e_number.data
    }
    with open(login + '.json', 'w') as outfile:
        json.dump(data, outfile)


@app.route('/form_second', methods=['GET', 'POST'])
def form_second():
    form = LoginFormSecond()

    if form.e_l_year.data is not None:

        if int(form.e_l_year.data) < 2015:
            regexForNumber = '^[A-Z]{2}$'
            lengthForSerion = 8
        else:
            regexForNumber = '^[A-Z][0-9]{2}$'
            lengthForSerion = 6

        form.d_f_e_series.validators = [Regexp(regex=regexForNumber,
                                               message=REGEXP.format(regexForNumber))]

        form.d_f_e_number.validators = [InputRequired(REQUIRED.format('number')),
                                        Length(min=lengthForSerion,
                                               max=lengthForSerion,
                                               message=LENGTH.format(lengthForSerion))]

    if form.validate_on_submit():
        writeToFile(form)
        return render_template("result.html",
                               form=form,
                               menu=App.getMenu())

    return render_template("form_second.html",
                           form=form,
                           menu=App.getMenu())


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
