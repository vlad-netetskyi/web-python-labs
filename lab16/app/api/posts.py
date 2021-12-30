from flask import g, request, jsonify, current_app, make_response
from flask_restful import Resource, Api, fields, marshal_with
from .. import db

from ..posts.models import Post

resourses = {
    'id': fields.Integer,
    'title': fields.String,
    'description': fields.String,
    'image': fields.String,
    'created': fields.DateTime,
    'is_enabled': fields.Boolean,
    'user_id': fields.Integer,
    'category_id': fields.Integer
}


class PostHandlerApi(Resource):
    @marshal_with(resourses)
    def get(self, id):
        return Post.query.get_or_404(id)

    @marshal_with(resourses)
    def post(self, id):
        data = request.get_json()['post']
        post_new = Post(
            title=data['title'],
            description=data['description'],
            image=data['image'],
            created=db.func.now(),
            is_enabled=data['is_enabled'],
            user_id=data['user_id'],
            category_id=data['category_id']
        )

        db.session.add(post_new)
        db.session.commit()
        return post_new

    @marshal_with(resourses)
    def put(self, id):
        data = request.get_json()['post']
        old = Post.query.get_or_404(id)
        new = Post(
            title=data['title'],
            description=data['description'],
            image=data['image'],
            user_id=data['user_id'],
            category_id=data['category_id']
        )
        old.title = new.title
        old.description = new.description
        old.image = new.image
        old.user_id = new.user_id
        old.category_id = new.category_id

        db.session.commit()
        return old

    def delete(self, id):
        p = Post.query.get(id)
        db.session.delete(p)
        db.session.commit()
        return jsonify({'message': 'The post has been deleted!'})


class PostAllHandlerApi(Resource):
    @marshal_with(resourses)
    def get(self):
        return Post.query.all()


api = Api(current_app)
api.add_resource(PostHandlerApi, "/api/v2/<int:id>")
api.add_resource(PostAllHandlerApi, "/api/v2/")
