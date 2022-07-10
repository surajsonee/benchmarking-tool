from .base import db


class Insulation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    material = db.Column(db.String(200), unique=False, nullable=False)   
    kvalue = db.Column(db.String(200), unique=False, nullable=False)
    building_id = db.Column(db.Integer, db.ForeignKey('building.id'))
    photo_id = db.Column(db.String(300), unique=False, nullable=False)
