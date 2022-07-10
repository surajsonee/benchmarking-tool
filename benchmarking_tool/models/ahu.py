from .base import db

class AHU(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    manufacturer = db.Column(db.String(200), unique=False, nullable = False)
    model_number = db.Column(db.String(200), unique = False, nullable = False)
    serial_number = db.Column(db.String(200), unique = False, nullable = False)
    year_built = db.Column(db.Integer, unique = False, nullable = False)
    cooling_capacity = db.Column(db.Float, unique = False, nullable = False)
    cooling_coil_type = db.Column(db.String(200), unique=False, nullable = False)
    heating_capacity = db.Column(db.Float, unique = False, nullable = False)
    heating_coil_type = db.Column(db.String(200), unique=False, nullable = False)
    effciency = db.Column(db.Integer, unique = False, nullable = False)
    contant_variable = db.Column(db.String(200), unique=False, nullable = False)
    area_id = db.Column(db.Integer, db.ForeignKey('area.id'))
    photo_id = db.Column(db.String(300), unique=False, nullable=False)
    building_id = db.Column(db.Integer, db.ForeignKey('building.id'))