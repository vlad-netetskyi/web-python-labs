from flask import render_template, flash, session
from .forms import LoginFormSecond
from .file_writer import writeToFile
from .. import App
from .custom_validator import validate


from . import form_blueprint


@form_blueprint.route('/form_second', methods=['GET', 'POST'])
def form_second():
    form = LoginFormSecond()
    validate(form=form)

    if form.validate_on_submit():
        writeToFile(form)
        flash('User has been written in json file')
        session['login'] = form.login.data
        session['e_l_number'] = form.e_l_number.data
        return render_template("form/result.html",
                               form=form,
                               menu=App.getMenu())

    return render_template("form/form_second.html",
                           form=form,
                           menu=App.getMenu())
