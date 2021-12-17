from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField,\
    SubmitField, SelectMultipleField
from wtforms.validators import Length, InputRequired
from flask_wtf.file import FileField, FileAllowed


class PostForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired(), Length(min=2, max=60)])
    description = TextAreaField('Text', validators=[Length(max=500)])
    image = FileField('Update Post Picture', validators=[FileAllowed(['jpg', 'png'])])
    category = SelectField('Category', validators=[InputRequired()])
    tags = SelectMultipleField("Tag", validators=[InputRequired()], coerce=int)
    submit = SubmitField('')
