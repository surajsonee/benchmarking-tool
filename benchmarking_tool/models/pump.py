from .base import db

class Pump(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    condition = db.Column(db.String(100), unique = False, nullable = False)
    head = db.Column(db.Float, unique = False,nullable = False)
    gpm = db.Column(db.Float, unique = False,nullable = False)
    area_id = db.Column(db.Integer, db.ForeignKey('area.id'))
    photo_id = db.Column(db.String(300), unique=False, nullable=False)
    building_id = db.Column(db.Integer, db.ForeignKey('building.id'))