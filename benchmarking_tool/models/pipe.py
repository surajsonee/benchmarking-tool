from .base import db

class Pipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pipe_type = db.Column(db.String(200), unique=False, nullable = False)
    pipe_finish = db.Column(db.String(200), unique=False, nullable = False)
    diameter= db.Column(db.Float, unique = False, nullable = False)
    length = db.Column(db.Float, unique = False, nullable = False)
    insulation_material = db.Column(db.String(200), unique = False, nullable = False)
    insulation_thickness = db.Column(db.Float(10), unique = False, nullable = False)
    area_id = db.Column(db.Integer, db.ForeignKey('area.id'))
    photo_id = db.Column(db.String(300), unique=False, nullable=False)
    building_id = db.Column(db.Integer, db.ForeignKey('building.id'))