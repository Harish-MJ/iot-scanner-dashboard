from . import db

class LaserData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String, nullable=False)
    measurements = db.Column(db.Text, nullable=False)

    def __init__(self, timestamp, measurements):
        self.timestamp = timestamp
        self.measurements = measurements
