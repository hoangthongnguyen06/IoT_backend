from app import app, db
from app.models.User import User
from app.models.Course import Course
from werkzeug.security import generate_password_hash

def create_sample_data():
    with app.app_context():
        # Tạo cơ sở dữ liệu và bảng
        db.create_all()

        # Thêm người dùng admin
        admin = User(username='admin', password=generate_password_hash('adminpassword'), is_admin=True)
        db.session.add(admin)

        # Thêm người dùng user1 và user2
        user1 = User(username='user1', password=generate_password_hash('user1password'), is_admin=False)
        user2 = User(username='user2', password=generate_password_hash('user2password'), is_admin=False)
        db.session.add_all([user1, user2])

        # Thêm khóa học
        course1 = Course(name='Course 1', description='Description for Course 1', user=admin)
        course2 = Course(name='Course 2', description='Description for Course 2', user=user1)
        course3 = Course(name='Course 3', description='Description for Course 3', user=user2)
        db.session.add_all([course1, course2, course3])

        # Lưu thay đổi vào cơ sở dữ liệu
        db.session.commit()

if __name__ == '__main__':
    create_sample_data()
