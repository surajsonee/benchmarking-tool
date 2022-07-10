from .base import db

class CommercialAppliance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appliance_type = db.Column(db.String(200), unique=False, nullable=False)
    quantity = db.Column(db.String(200), unique=False, nullable=False)
    wattage = db.Column(db.String(200), unique=False, nullable=False)
    area_id = db.Column(db.Integer, db.ForeignKey('area.id'))
    photo_id = db.Column(db.String(300), unique=False, nullable=False)
    building_id = db.Column(db.Integer, db.ForeignKey('building.id'))

