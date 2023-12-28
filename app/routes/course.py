from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.course import course_exam_association
from app import db
from random import shuffle

course_bp = Blueprint('course', __name__)

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.course import Course
from app.models.user import User
from app.models.exam import Exam, user_exam_association
from app.models.device import Device
from app.models.exploit import Exploit
from app.models.cve import CVE
from app.models import db

course_bp = Blueprint('course', __name__)

# @course_bp.route('/courses', methods=['POST'])
# @jwt_required()
# def create_course():
#     current_user = get_jwt_identity()
#     if current_user['role'] == 'admin':
#         current_user = get_jwt_identity()
#         if current_user['role'] == 'admin':
#             data = request.get_json()
#             new_course = Course(
#                 name=data['name'],
#                 description=data['description'],
#                 start_time=data['start_time'],
#                 end_time=data['end_time']
#             )
#             db.session.add(new_course)
#             db.session.commit()
#             return jsonify({'message': 'Course created successfully'})
#         else:
#             return jsonify({'message': 'Unauthorized'}), 403
#     else:
#         return jsonify({'message': 'Unauthorized'}), 403

@course_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def get_statistics():
    current_user = get_jwt_identity()

    if current_user['role'] == 'admin':
    # Lấy tổng số thiết bị
        total_devices = Device.query.count()

        # Lấy tổng số CVE
        total_cves = CVE.query.count()

        # Lấy tổng số exploit
        total_exploits = Exploit.query.count()

        return jsonify({
            'total_devices': total_devices,
            'total_cves': total_cves,
            'total_exploits': total_exploits
        })
@course_bp.route('/courses', methods=['POST'])
@jwt_required()
def create_course():
    current_user = get_jwt_identity()

    if current_user['role'] == 'admin':
        data = request.get_json()

        # Tạo khóa học mới
        new_course = Course(
            name=data['name'],
            description=data['description'],
            start_time=data['start_time'],
            end_time=data['end_time']
        )
        db.session.add(new_course)
        db.session.commit()

        # Lấy id của khóa học mới tạo
        course_id = new_course.id

        # Lấy danh sách người dùng từ request
        user_ids = data.get('user_ids', [])

        # Lấy danh sách đề thi từ cơ sở dữ liệu
        all_exams = Exam.query.all()

        # Kiểm tra xem có đề thi nào không
        if not all_exams:
            return jsonify({'message': 'No exams available'}), 400

        # Lấy số lượng người dùng cần gán
        num_users_to_assign = len(user_ids)

        # Kiểm tra xem có đủ đề thi để gán không
        if num_users_to_assign > len(all_exams):
            return jsonify({'message': 'Not enough exams available for assignment'}), 400

        # Trộn ngẫu nhiên danh sách đề thi
        shuffle(all_exams)

        # Gán đề thi cho từng người dùng
        for user_id, assigned_exam in zip(user_ids, all_exams):
            # Thêm bản ghi mới vào bảng liên kết
            course_exam_association_record = course_exam_association.insert().values(
                course_id=course_id,
                exam_id=assigned_exam.id
            )
            db.session.execute(course_exam_association_record)

            # Thêm bản ghi mới vào bảng liên kết user_exam_association
            user_exam_association_record = user_exam_association.insert().values(
                user_id=user_id,
                exam_id=assigned_exam.id,
                score=None  # Đặt giá trị mặc định cho điểm số
            )
            db.session.execute(user_exam_association_record)

            user = User.query.get(user_id)
            user.course_id = course_id

        db.session.commit()

        return jsonify({'message': 'Course created successfully with users and exams'})
    else:
        return jsonify({'message': 'Unauthorized'}), 403
    
@course_bp.route('/courses', methods=['GET'])
@jwt_required()
def get_courses():
    current_user = get_jwt_identity()
    if current_user['role'] == 'admin':
        courses = Course.query.all()
        courses_data = []

        for course in courses:
            # Lấy danh sách người tham gia khóa học
            users_in_course = [{'id': user.id, 'username': user.username, 'full_name':user.full_name} for user in course.users]

            # Lấy danh sách đề thi trong khóa học
            exams_in_course = [{'id': exam.id} for exam in course.exams]

            course_data = {
                'id': course.id,
                'name': course.name,
                'description': course.description,
                'start_time': course.start_time, 
                'end_time': course.end_time,
                'users': users_in_course,
                'exams': exams_in_course
            }

            courses_data.append(course_data)

        return jsonify({'courses': courses_data})
    else:
        return jsonify({'message': 'Unauthorized'}), 403
    
@course_bp.route('/course/<int:user_id>', methods=['GET'])
@jwt_required()
def get_courses_by_user(user_id):
    current_user = get_jwt_identity()
    
    if current_user['role'] == 'user':
        user = User.query.get(user_id)
        if user:
            courses = Course.query.filter_by(id=user.course_id).all()

            user_courses = [{'id': course.id, 'name': course.name, 'description': course.description, 'start_time': course.start_time, 'end_time': course.end_time } for course in courses]

            return jsonify({'user_courses': user_courses})
        else:
            return jsonify({'message': 'User not found'}), 404
    else:
        return jsonify({'message': 'Unauthorized'}), 403


@course_bp.route('/courses/<int:course_id>', methods=['GET'])
@jwt_required()
def get_course(course_id):
    course = Course.query.get(course_id)
    if course:
        users_in_course = [{'id': user.id, 'username': user.username} for user in course.users]

        # Lấy danh sách đề thi trong khóa học
        exams_in_course = [{'id': exam.id} for exam in course.exams]
        course_data = {
            'id': course.id,
            'name': course.name,
            'description': course.description,
            'start_time': course.start_time, 
            'end_time': course.end_time,
            'users': users_in_course,
            'exams': exams_in_course
        }
        return jsonify({'course': course_data})
    else:
        return jsonify({'message': 'Course not found'}), 404

@course_bp.route('/course_results/<int:course_id>', methods=['GET'])
def get_course_results(course_id):
    # Lấy thông tin khóa thi
    course = Course.query.get(course_id)
    
    if not course:
        return jsonify({'message': 'Course not found'}), 404

    # Lấy danh sách các đề thi thuộc khóa thi
    exams = db.session.query(Exam).join(course_exam_association).filter(course_exam_association.c.course_id == course_id).all()

    # Tạo danh sách kết quả
    results = []
    for exam in exams:
        # Lấy thông tin người thi, điểm và thông tin từ bảng Device
        user_results = db.session.query(User.username, Device.name, Device.ip_address, user_exam_association.c.score).\
            join(user_exam_association, User.id == user_exam_association.c.user_id).\
            join(Device, Device.id == exam.device_id).\
            filter(user_exam_association.c.exam_id == exam.id).all()

        # Thêm thông tin vào danh sách kết quả
        result_data = {
            'exam_id': exam.id,
            'results': [{'username': username, 'device_name': device_name, 'score': score, 'ip_address':ip_address} 
                        for username, device_name, ip_address, score in user_results]
        }
        results.append(result_data)

    # Tạo kết quả tổng hợp
    course_result = {
        'course_name': course.name,
        'results': results
    }

    return jsonify(course_result)

@course_bp.route('/courses/<int:course_id>', methods=['PUT'])
@jwt_required()
def update_course(course_id):
    current_user = get_jwt_identity()
    if current_user['role'] == 'admin':
        course = Course.query.get(course_id)
        if course:
            data = request.get_json()
            course.name = data['name']
            course.description = data['description']
            course.start_time=data['start_time']
            course.end_time=data['end_time']
            db.session.commit()
            return jsonify({'message': 'Course updated successfully'})
        else:
            return jsonify({'message': 'Course not found'}), 404
    else:
        return jsonify({'message': 'Unauthorized'}), 403

@course_bp.route('/courses/<int:course_id>/update', methods=['POST'])
@jwt_required()
def add_user_and_exam_to_course(course_id):
    try:
        current_user = get_jwt_identity()

        if current_user['role'] == 'admin':
            data = request.get_json()

            # Lấy danh sách người dùng và đề thi từ request
            user_ids = data.get('user_ids', [])
            exam_ids = data.get('exam_ids', [])

            # Lấy đối tượng Course từ cơ sở dữ liệu
            course = Course.query.get(course_id)

            if course:
                # Lấy danh sách đề thi và người dùng từ cơ sở dữ liệu
                exams = Exam.query.filter(Exam.id.in_(exam_ids)).all()
                users = User.query.filter(User.id.in_(user_ids)).all()

                # Trộn ngẫu nhiên danh sách đề thi để gán cho người dùng
                shuffle(exams)

                # Gán đề thi cho từng người dùng
                for user in users:
                    # Kiểm tra xem có đề thi nào còn lại không
                    if exams:
                        # Lấy đề thi đầu tiên từ danh sách đã trộn
                        assigned_exam = exams.pop(0)
                        # Thêm bản ghi mới vào bảng liên kết
                        course_exam_association_record = course_exam_association.insert().values(
                            course_id=course.id,
                            exam_id=assigned_exam.id
                        )
                        db.session.execute(course_exam_association_record)

                        # Thêm bản ghi mới vào bảng liên kết user_exam_association
                        user_exam_association_record = user_exam_association.insert().values(
                            user_id=user.id,
                            exam_id=assigned_exam.id,
                            score=None  # Đặt giá trị mặc định cho điểm số
                        )
                        db.session.execute(user_exam_association_record)

                        user.course_id = course_id

                db.session.commit()

                return jsonify({'message': 'Exams assigned to users successfully'})
            else:
                return jsonify({'message': 'Course not found'}), 404
        else:
            return jsonify({'message': 'Unauthorized'}), 403
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error assigning exams to users: {str(e)}'}), 500
    
@course_bp.route('/courses/<int:course_id>', methods=['DELETE'])
@jwt_required()
def delete_course(course_id):
    current_user = get_jwt_identity()
    if current_user['role'] == 'admin':
        course = Course.query.get(course_id)
        if course:
            db.session.delete(course)
            db.session.commit()
            return jsonify({'message': 'Course deleted successfully'})
        else:
            return jsonify({'message': 'Course not found'}), 404
    else:
        return jsonify({'message': 'Unauthorized'}), 403
