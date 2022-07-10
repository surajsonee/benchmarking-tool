from .base import db

class UnitVentilator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    supply_air_temp = db.Column(db.Float, unique = False, nullable = False)
    outdoor_air_setpoint =  db.Column(db.Float, unique = False, nullable = False)
    manufacturer = db.Column(db.String(200), unique=False, nullable = False)
    model_number = db.Column(db.String(200), unique = False, nullable = False)
    serial_number = db.Column(db.String(200), unique = False, nullable = False)
    year_built = db.Column(db.Integer, unique = False, nullable = False)
    cooling_capacity = db.Column(db.Float, unique = False, nullable = False)
    cooling_coil_type = db.Column(db.String(200), unique=False, nullable = False)
    heating_capacity = db.Column(db.Float, unique = False, nullable = False)
    heating_coil_type = db.Column(db.String(200), unique=False, nullable = False)
    supply_cfm = db.Column(db.Float, unique = False, nullable = False)
    area_id = db.Column(db.Integer, db.ForeignKey('area.id'))
    photo_id = db.Column(db.String(300), unique=False, nullable=False)
    building_id = db.Column(db.Integer, db.ForeignKey('building.id'))
