from flask import Blueprint, jsonify, request, redirect, session, url_for, flash
from app.models.exam_result import ExamResult
from app.models import db

exam_result_bp = Blueprint('exam_result', __name__)

@exam_result_bp.route('/exam_results', methods=['GET'])
def get_exam_results():
    exam_results = ExamResult.query.all()
    exam_results_data = [{'id': result.id, 'user_id': result.user_id, 'exam_id': result.exam_id, 'score': result.score, 'submission_time': result.submission_time} for result in exam_results]
    return jsonify({'exam_results': exam_results_data})

@exam_result_bp.route('/exam_results', methods=['POST'])
def create_exam_result():
    data = request.get_json()
    new_exam_result = ExamResult(user_id=data['user_id'], exam_id=data['exam_id'], score=data['score'])
    db.session.add(new_exam_result)
    db.session.commit()
    return jsonify({'message': 'Exam result created successfully'})

@exam_result_bp.route('/exam_results/<int:result_id>', methods=['PUT'])
def update_exam_result(result_id):
    exam_result = ExamResult.query.get(result_id)
    if exam_result:
        data = request.get_json()
        exam_result.user_id = data['user_id']
        exam_result.exam_id = data['exam_id']
        exam_result.score = data['score']
        db.session.commit()
        return jsonify({'message': 'Exam result updated successfully'})
    else:
        return jsonify({'message': 'Exam result not found'}), 404

@exam_result_bp.route('/exam_results/<int:result_id>', methods=['DELETE'])
def delete_exam_result(result_id):
    exam_result = ExamResult.query.get(result_id)
    if exam_result:
        db.session.delete(exam_result)
        db.session.commit()
        return jsonify({'message': 'Exam result deleted successfully'})
    else:
        return jsonify({'message': 'Exam result not found'}), 404

def create_exam_result_blueprint():
    return exam_result_bp
