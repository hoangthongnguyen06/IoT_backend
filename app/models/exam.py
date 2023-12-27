from app.models import db
from datetime import datetime, timedelta
from app.models.course import course_exam_association
user_exam_association = db.Table(
    'user_exam_association',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('exam_id', db.Integer, db.ForeignKey('exams.id')),
    db.Column('score',db.Float, nullable=True ),
    db.Column('exam_answer_path', db.String(255), nullable=True)
)
class Exam(db.Model):
    __tablename__ = "exams"
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'), nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=True)
    exam_duration = db.Column(db.Interval, nullable=False, default=timedelta(minutes=60))
    # user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True, unique=True)
    # Quan hệ với Course và User
    
     # Quan hệ với Course (Nhiều-nhiều)
    courses = db.relationship('Course', secondary=course_exam_association, back_populates='exams')
    users = db.relationship('User', secondary=user_exam_association, back_populates='exams')
