from app.models import db

class CVE(db.Model):
    __tablename__ = "cves"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    score = db.Column(db.Float)  # Thêm trường "điểm của CVE"
    severity = db.Column(db.String(20))  # Thêm trường "mức độ của CVE"

    def __init__(self, name, description, score):
        self.name = name
        self.description = description
        self.score = score
        self.calculate_severity() 

    def calculate_severity(self):
        self.score = float(self.score)
        if self.score < 4:
            self.severity = "Không nghiêm trọng"
        elif 4 <= self.score < 7:
            self.severity = "Thấp"
        elif 7 <= self.score < 9:
            self.severity = "Cao"
        else:
            self.severity = "Nghiêm trọng"
    