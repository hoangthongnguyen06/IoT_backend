from flask import Blueprint, jsonify, request, redirect, session, url_for, flash
from app.models.exam import Exam
from app.models import db

exam_bp = Blueprint('exam', __name__)

@exam_bp.route('/exams', methods=['GET'])
def get_exams():
    exams = Exam.query.all()
    exams_data = [{'id': exam.id, 'course_id': exam.course_id, 'device_id': exam.device_id, 'start_time': exam.start_time, 'end_time': exam.end_time} for exam in exams]
    return jsonify({'exams': exams_data})

@exam_bp.route('/exams', methods=['POST'])
def create_exam():
    data = request.get_json()
    new_exam = Exam(course_id=data['course_id'], device_id=data['device_id'], start_time=data['start_time'], end_time=data['end_time'])
    db.session.add(new_exam)
    db.session.commit()
    return jsonify({'message': 'Exam created successfully'})

@exam_bp.route('/exams/<int:exam_id>', methods=['PUT'])
def update_exam(exam_id):
    exam = Exam.query.get(exam_id)
    if exam:
        data = request.get_json()
        exam.course_id = data['course_id']
        exam.device_id = data['device_id']
        # ... thêm các field khác
        db.session.commit()
        return jsonify({'message': 'Exam updated successfully'})
    else:
        return jsonify({'message': 'Exam not found'}), 404

@exam_bp.route('/exams/<int:exam_id>', methods=['DELETE'])
def delete_exam(exam_id):
    exam = Exam.query.get(exam_id)
    if exam:
        db.session.delete(exam)
        db.session.commit()
        return jsonify({'message': 'Exam deleted successfully'})
    else:
        return jsonify({'message': 'Exam not found'}), 404
