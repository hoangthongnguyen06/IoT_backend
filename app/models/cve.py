from app.models import db

class CVE(db.Model):
    __tablename__ = "cves"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    