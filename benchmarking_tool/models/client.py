from .base import db
from datetime import datetime
from .building import *


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    company = db.Column(db.String(80), unique=False, nullable=False)
    first_name = db.Column(db.String(80), unique=False, nullable=False)
    last_name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(150), unique=False, nullable=False)
    address = db.Column(db.String(200), unique=False, nullable=False)
    province = db.Column(db.String(200), unique=False, nullable=False)
    postal_code = db.Column(db.String(200), unique=False, nullable=False)
    buildings = db.relationship('Building', backref='owner')
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    photo_id = db.Column(db.String(300), unique=False, nullable=False)