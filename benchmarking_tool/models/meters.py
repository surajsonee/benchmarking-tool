from .base import db


class Meter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    distributer = db.Column(db.String(200), unique=False, nullable=False)
    meter_number = db.Column(db.String(200), unique=True,
                             nullable=False)
    account_number = db.Column(db.String(200), unique=False, nullable=False)
    energy_type = db.Column(db.String(200), unique=False, nullable=False)
    building_id = db.Column(db.Integer, db.ForeignKey('building.id'))