from flask import Flask, g, request, jsonify
from functools import wraps
from ..instructors.models import Teacher
from .. import db

from . import instructors_api_blueprint

api_username = 'admin'
api_password = 'password'


def protected(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth and auth.username == api_username and auth.password == api_password:
            return f(*args, **kwargs)
        return jsonify({'message': 'Authentication failed!'}), 403

    return decorated


@instructors_api_blueprint.route('/teachers', methods=['GET'])
@protected
def get_teachers():
    teachers = Teacher.query.all()
    return_values = [{"id": teacher.id,
                      "first_name": teacher.first_name,
                      "last_name": teacher.last_name,
                      "surname": teacher.surname,
                      "position_id": teacher.position_id,
                      "start_work": teacher.start_work,
                      "chair": teacher.chair,
                      "number_phone": teacher.number_phone} for teacher in teachers]

    return jsonify({'Teachers': return_values})


@instructors_api_blueprint.route('/teacher/<int:id>', methods=['GET'])
@protected
def get_teacher(id):
    teacher = Teacher.query.get_or_404(id)
    return jsonify({"id": teacher.id,
                    "first_name": teacher.first_name,
                    "last_name": teacher.last_name,
                    "surname": teacher.surname,
                    "position_id": teacher.position_id,
                    "start_work": teacher.start_work,
                    "chair": teacher.chair,
                    "number_phone": teacher.number_phone})


@instructors_api_blueprint.route('/teacher', methods=['POST'])
def add_teacher():
    new_institution_data = request.get_json()

    instructor = Teacher(
        first_name=new_institution_data['first_name'],
        last_name=new_institution_data['last_name'],
        surname=new_institution_data['surname'],
        position_id=new_institution_data['position_id'],
        start_work=new_institution_data['start_work'],
        chair=new_institution_data['chair'],
        number_phone=new_institution_data['number_phone']
    )

    db.session.add(instructor)
    db.session.commit()
    return jsonify({"id": instructor.id,
                    "first_name": instructor.first_name,
                    "last_name": instructor.last_name,
                    "surname": instructor.surname,
                    "position_id": instructor.position_id,
                    "start_work": instructor.start_work,
                    "chair": instructor.chair,
                    "number_phone": instructor.number_phone})


@instructors_api_blueprint.route('/teacher/<int:id>', methods=['PUT', 'PATCH'])
@protected
def edit_teacher(id):
    teacher = Teacher.query.get(id)
    if not teacher:
        return jsonify({"Message": "Teacher does not exist"})

    update_data = request.get_json()

    teacher.first_name = update_data['first_name']
    teacher.last_name = update_data['last_name']
    teacher.surname = update_data['surname']
    teacher.position_id = update_data['position_id']
    teacher.start_work = update_data['start_work']
    teacher.chair = update_data['chair']
    teacher.number_phone = update_data['number_phone']

    db.session.add(teacher)
    db.session.commit()

    return jsonify({"id": teacher.id,
                    "first_name": teacher.first_name,
                    "last_name": teacher.last_name,
                    "surname": teacher.surname,
                    "position_id": teacher.position_id,
                    "start_work": teacher.start_work,
                    "chair": teacher.chair,
                    "number_phone": teacher.number_phone})


@instructors_api_blueprint.route('/teacher/<int:id>', methods=['DELETE'])
@protected
def delete_teacher(id):
    teacher = Teacher.query.get_or_404(id)
    db.session.delete(teacher)
    db.session.commit()

    return jsonify({'Message': 'The teacher has been deleted!'})

