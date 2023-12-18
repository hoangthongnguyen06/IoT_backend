from app.models import db

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    cve_id = db.Column(db.Integer, db.ForeignKey('cve.id'))
