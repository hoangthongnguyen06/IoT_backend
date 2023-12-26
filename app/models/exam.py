from app.models import db
from datetime import datetime, timedelta
from app.models.course import course_exam_association

class Exam(db.Model):
    __tablename__ = "exams"
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=True)
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'), nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    exam_duration = db.Column(db.Interval, nullable=False, default=timedelta(minutes=60))
    score = db.Column(db.Float, nullable=True)  # Thêm trường điểm

    # Quan hệ với Course và User
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True, unique=True)

     # Quan hệ với Course (Nhiều-nhiều)
    courses = db.relationship('Course', secondary=course_exam_association, back_populates='exams')
    user = db.relationship('User', back_populates='exam')
