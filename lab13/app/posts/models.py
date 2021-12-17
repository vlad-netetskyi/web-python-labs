import enum

from .. import db
# from sqlalchemy.types import Enum


class PostType(enum.Enum):
    News = 'News'
    Publication = 'Publication'
    Other = 'Other'


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image = db.Column(db.String(20), nullable=False, default='default_post.png')
    created = db.Column(db.DateTime, default=db.func.now())
    type = db.Column(db.Enum(PostType))
    is_enabled = db.Column(db.Boolean, default=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
