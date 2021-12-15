from flask import Markup
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, BooleanField
from wtforms.validators import DataRequired, InputRequired, Length, AnyOf, Regexp, EqualTo, Email, ValidationError
from .models import User


REQUIRED = 'A {} is required!'
LENGTH_BETWEEN = 'length must be between {} and {} characters'
LENGTH_MIN = 'length must be at least {} characters'
LENGTH = 'length must be {} characters'
REGEXP = 'input must be for regex ({})'
PASSWORD = 'passwords must match'
ONLY_USERNAME_SYMBOLS = 'username must have only letters, numbers, . or _'
EMAIL = 'Email must be in pattern for email'
EMAIL_EXIST = 'This email already exist!'
USERNAME_EXIST = 'This username already exist!'


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


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[InputRequired(REQUIRED.format('username')),
                                       Length(min=4, max=14, message=LENGTH_BETWEEN.format(4, 14)),
                                       Regexp('^[A-Za-z][A-Za-z0-9_.]+$', message=ONLY_USERNAME_SYMBOLS)])
    email = StringField('Email',
                        validators=[InputRequired(REQUIRED.format('email')),
                                    Email(message=EMAIL)])
    password = PasswordField('Password',
                             validators=[InputRequired(REQUIRED.format('password')),
                                         Length(min=6, message=LENGTH_MIN.format(6))])

    password_repeat = PasswordField('Confirm password',
                                    validators=[InputRequired(REQUIRED.format('password')),
                                                Length(min=6, message=LENGTH_MIN.format(6)),
                                                EqualTo('password')])

    submit = SubmitField(label=(''))

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(EMAIL_EXIST)

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(USERNAME_EXIST)


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(EMAIL)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField(label=Markup('<div class="form-check-label">Remember me</div>'))
    submit = SubmitField(label=(''))
