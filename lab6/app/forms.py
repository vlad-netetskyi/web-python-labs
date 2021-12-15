from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import InputRequired, Length, AnyOf, Regexp, EqualTo


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
                                         AnyOf(values=['password', 'secret'])])


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