from .base import db

class CommercialDHW(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    equipment_type = db.Column(db.String(200), unique=False, nullable=False)
    tag = db.Column(db.String(200), unique=False, nullable=False)
    manufacturer = db.Column(db.String(200), unique=False, nullable=False)
    model_number = db.Column(db.String(200), unique=False, nullable=False)
    serial_number = db.Column(db.String(200), unique=False, nullable=False)
    input_capacity = db.Column(db.Integer, unique=False, nullable=False)
    fuel_type = db.Column(db.String(200), unique=False, nullable=False)
    efficiency = db.Column(db.Integer, unique=False, nullable=False)
    storage_volume = db.Column(db.Integer, unique=False, nullable=False)
    set_point = db.Column(db.Integer, unique=False, nullable=False)
    area_id = db.Column(db.Integer, db.ForeignKey('area.id'))
    building_id = db.Column(db.Integer, db.ForeignKey('building.id'))
    photo_id = db.Column(db.String(300), unique=False, nullable=False)