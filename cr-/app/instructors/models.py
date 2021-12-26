from app import db


class Position(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    teachers = db.relationship('Teacher', backref='position', lazy=True)


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    position_id = db.Column(db.Integer, db.ForeignKey('position.id'), nullable=False)
    start_work = db.Column(db.DateTime, default=db.func.now())
    chair = db.Column(db.String(50), nullable=False)
    number_phone = db.Column(db.String(13), nullable=False)
