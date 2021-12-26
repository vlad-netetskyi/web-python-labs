from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length, Regexp
from .forms import REGEXP, LENGTH, REQUIRED


def validate(form: FlaskForm):
    if form.e_l_year.data is not None:
        regexForNumber = ''
        lengthForSerion = ''

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
