from flask import Blueprint

instructors_blueprint = Blueprint('teacher', __name__, template_folder="templates/instructors")

from . import controller
