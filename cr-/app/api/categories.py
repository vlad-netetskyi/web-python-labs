from flask import g, request, jsonify, current_app
from .. import db
from functools import wraps

from ..posts.models import Category
from . import api_blueprint

api_username = 'admin'
api_password = 'password'


def protected(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth and auth.username == api_username \
           and auth.password == api_password:
            return f(*args, **kwargs)
        return jsonify({'message': 'Authentication failed!'}), 403
    return decorated


@api_blueprint.route('/category', methods=['GET'])
@protected
def get_categories():
    _ = 'select id, name from category'
    categories = Category.query.all()

    return_values = []

    for category in categories:
        category_dict = {}
        category_dict['id'] = category.id
        category_dict['name'] = category.name

        return_values.append(category_dict)

    return jsonify({'categories' : return_values})


@api_blueprint.route('/category/<int:category_id>', methods=['GET'])
@protected
def get_category(category_id):
    category = Category.query.get_or_404(category_id)
    return jsonify({'category' : 
                    {'id': category.id, 
                     'name' : category.name}})


@api_blueprint.route('/category', methods=['POST'])
@protected
def add_category():
    name = request.get_json()['category']['name']

    categories = Category.query.all()
    for cat in categories:
        if cat.name == name:
            return jsonify({'message': f'The category "{name}" already exist!'})

    new_category = Category(name=name)
    db.session.add(new_category)
    db.session.commit()

    return get_category(new_category.id)


@api_blueprint.route('/category/<int:category_id>', methods=['PUT', 'PATCH'])
@protected
def edit_category(category_id):
    name = request.get_json()['category']['name']

    categories = Category.query.all()
    for cat in categories:
        if cat.name == name:
            return jsonify({'message': f'The category "{name}" already exist!'})

    category = Category.query.get_or_404(category_id)
    category.name = name
    db.session.commit()

    return jsonify({'category':
                    {'id': category.id,
                     'name': category.name}})


@api_blueprint.route('/category/<int:category_id>', methods=['DELETE'])
@protected
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return jsonify({'message': 'The category has been deleted!'})
