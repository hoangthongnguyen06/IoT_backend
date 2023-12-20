from app.models import db

class CVE(db.Model):
    __tablename__ = "cves"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    exploit_path = db.Column(db.String(200), nullable=False)
