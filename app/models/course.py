from app.models import db
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event

course_exam_association = db.Table(
    'course_exam_association',
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id')),
    db.Column('exam_id', db.Integer, db.ForeignKey('exams.id'))
)
class Course(db.Model):
    __tablename__ = "courses"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    start_time = db.Column(db.TIMESTAMP, nullable=True)  # Thời gian bắt đầu
    end_time = db.Column(db.TIMESTAMP, nullable=True)    # Thời gian kết thúc
    # Quan hệ với Exam
    exams = db.relationship('Exam', secondary=course_exam_association, back_populates='courses')
    users = db.relationship('User', back_populates='course')
    status = db.Column(db.String(20), default='Chưa thi', nullable=True)  # Thêm trường status

    def update_status(self):
            current_time = datetime.now()

            if self.start_time <= current_time <= self.end_time:
                self.status = 'Đang diễn ra'
            elif current_time < self.start_time:
                self.status = 'Chưa diễn ra'
            else:
                self.status = 'Đã kết thúc'

