from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField,\
    SubmitField, SelectMultipleField, DateTimeField, DateField
from wtforms.validators import Length, InputRequired
from flask_wtf.file import FileField, FileAllowed


class PostForm(FlaskForm):
    first_name = StringField('First name', validators=[InputRequired(), Length(min=2, max=60)])
    last_name = StringField('Last name', validators=[InputRequired(), Length(min=2, max=60)])
    chair = StringField('Chair', validators=[InputRequired(), Length(min=2, max=60)])
    surname = StringField('Surname', validators=[InputRequired(), Length(min=2, max=60)])
    position = SelectField('Position', validators=[InputRequired()])
    start_work = DateField('Start Work', validators=[InputRequired()])
    number_phone = StringField('Last name', validators=[InputRequired(), Length(min=13, max=14)])
    submit = SubmitField('')
