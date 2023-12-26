from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from app.models.course import course_exam_association
from app import db

course_bp = Blueprint('course', __name__)

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.course import Course
from app.models.user import User
from app.models.exam import Exam
from app.models import db

course_bp = Blueprint('course', __name__)

@course_bp.route('/courses', methods=['POST'])
@jwt_required()
def create_course():
    current_user = get_jwt_identity()
    if current_user['role'] == 'admin':
        current_user = get_jwt_identity()
        if current_user['role'] == 'admin':
            data = request.get_json()
            new_course = Course(
                name=data['name'],
                description=data['description'],
            )
            db.session.add(new_course)
            db.session.commit()
            return jsonify({'message': 'Course created successfully'})
        else:
            return jsonify({'message': 'Unauthorized'}), 403
    else:
        return jsonify({'message': 'Unauthorized'}), 403
    
@course_bp.route('/courses', methods=['GET'])
@jwt_required()
def get_courses():
    courses = Course.query.all()
    courses_data = []

    for course in courses:
        # Lấy danh sách người tham gia khóa học
        users_in_course = [{'id': user.id, 'username': user.username} for user in course.users]

        # Lấy danh sách đề thi trong khóa học
        exams_in_course = [{'id': exam.id, 'score': exam.score} for exam in course.exams]

        course_data = {
            'id': course.id,
            'name': course.name,
            'description': course.description,
            'users': users_in_course,
            'exams': exams_in_course
        }

        courses_data.append(course_data)

    return jsonify({'courses': courses_data})

@course_bp.route('/course/<int:user_id>', methods=['GET'])
@jwt_required()
def get_courses_by_user(user_id):
    current_user = get_jwt_identity()
    
    if current_user['role'] == 'user':
        user = User.query.get(user_id)
        if user:
            courses = Course.query.filter_by(id=user.course_id).all()

            user_courses = [{'id': course.id, 'name': course.name, 'description': course.description} for course in courses]

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
        course_data = {'id': course.id, 'name': course.name, 'description': course.descriptio, 'exams':course.exams[0]}
        return jsonify({'course': course_data})
    else:
        return jsonify({'message': 'Course not found'}), 404


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

            # Lấy đối tượng Course từ cơ sở dữ liệu
            course = Course.query.get(course_id)

            if course:
                # Kiểm tra sự tồn tại của Exam và User
                exam_id = data.get('exam_id')
                user_id = data.get('user_id')

                exam = Exam.query.get(exam_id)
                user = User.query.get(user_id)

                if exam and user:
                    course_exam_association_record = course_exam_association.insert().values(
                        course_id=course.id,
                        exam_id=exam.id
                    )
                    db.session.execute(course_exam_association_record)

                    user.course_id = course_id

                    db.session.commit()

                    return jsonify({'message': 'User and Exam added to course successfully'})
                else:
                    return jsonify({'message': 'Exam or User not found'}), 404
            else:
                return jsonify({'message': 'Course not found'}), 404
        else:
            return jsonify({'message': 'Unauthorized'}), 403
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error adding User and Exam to course: {str(e)}'}), 500
    
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
