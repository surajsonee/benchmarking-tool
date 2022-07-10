from .base import db

class Utility_Bill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    usage = db.Column(db.Integer)
    cost = db.Column(db.Integer)
    meter_number = db.Column(db.Integer)



    def __init__(self, start_date, end_date, usage, cost, meter_number):
        self.start_date = start_date
        self.end_date = end_date

        self.usage = usage
        self.cost = cost
        self.meter_number = meter_number

    def __repr__(self):
        return '<Utility_Bill %r>' % self.id

