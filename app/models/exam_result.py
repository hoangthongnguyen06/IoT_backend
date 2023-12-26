from app.models import db

class ExamResult(db.Model):
    __tablename__ = "exam_results"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'), nullable=False)
    score = db.Column(db.Float, nullable=False)
    submission_time = db.Column(db.TIMESTAMP, nullable=False, default=db.func.current_timestamp())
