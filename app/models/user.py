from app.models import db
from app.models.exam import user_exam_association
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    unit_id = db.Column(db.Integer, db.ForeignKey('units.id'))
    role = db.Column(db.String(20), nullable=False, check_constraint="role IN ('admin', 'user')")
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=True)
    # Quan hệ với Exam
    exams = db.relationship('Exam', secondary=user_exam_association, back_populates='users', uselist=False)
    course = db.relationship('Course', back_populates='users')