from .base import db


class Foundation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    foundationtype = db.Column(db.String(200), unique=False, nullable=False)
    material = db.Column(db.String(200), unique=False, nullable=False)
    rx = db.Column(db.String(200), unique=False, nullable=False)
    rvalue = db.Column(db.String(200), unique=False, nullable=False)
    building_id = db.Column(db.Integer, db.ForeignKey('building.id'))
    photo_id = db.Column(db.String(300), unique=False, nullable=False)
