roof_types = [['Brick Veneer', 1.2], ['Concrete Block', 1.28], ['Fiberglass Paneling', 1], ['Poured Concrete', 1.28], [
    'Steel Paneling', 0.61], ['Stone Aggregate', 1], ['Stucco', 0.12], ['Vinyl Paneling', 0.9]]


Class Static_Roof(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    roof_type = db.Column(db.Str(roof_types))
