from flask import Blueprint

instructors_api_blueprint = Blueprint('teacher_api', __name__)

from . import controller
