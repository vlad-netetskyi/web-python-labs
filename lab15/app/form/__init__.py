from flask import Blueprint

form_blueprint = Blueprint('form', __name__, template_folder="templates")

from . import controller
