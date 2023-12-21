from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from app.models import course
from app.models import user
from app import db

course_bp = Blueprint('course', __name__)

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.course import Course
from app.models import db

course_bp = Blueprint('course', __name__)

@course_bp.route('/courses', methods=['POST'])
@jwt_required()
def create_course():
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
    
@course_bp.route('/courses', methods=['GET'])
def get_courses():
    courses = Course.query.all()
    courses_data = [{'id': course.id, 'name': course.name, 'description': course.description} for course in courses]
    return jsonify({'courses': courses_data})


@course_bp.route('/courses/<int:course_id>', methods=['GET'])
def get_course(course_id):
    course = Course.query.get(course_id)
    if course:
        course_data = {'id': course.id, 'name': course.name, 'description': course.description}
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
