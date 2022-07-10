from .base import db


class Light(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fixture_count = db.Column(db.Integer, unique=False, nullable=False)
    hours = db.Column(db.Integer, unique=False,
                      nullable=False)
    fixture = db.Column(db.String(200), unique=False, nullable=False)
    lamp = db.Column(db.String(200), unique=False, nullable=False)
    wattage = db.Column(db.Integer, unique=False, nullable=False)
    lamp_count = db.Column(db.Integer, unique=False, nullable=False)
    area_id = db.Column(db.Integer, db.ForeignKey('area.id'))
    photo_id = db.Column(db.String(300), unique=False, nullable=False)
    building_id = db.Column(db.Integer, db.ForeignKey('building.id'))