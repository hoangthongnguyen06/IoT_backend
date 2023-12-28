from app.models import db
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
