from .base import db


class ExteriorWall(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    material = db.Column(db.String(200), unique=False, nullable=False)    
    rvalue = db.Column(db.String(200), unique=False, nullable=False)
    building_id = db.Column(db.Integer, db.ForeignKey('building.id'))
    photo_id = db.Column(db.String(300), unique=False, nullable=False)