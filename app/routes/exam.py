from flask import Blueprint, jsonify, request
from app.models.exam import Exam
from app.models.device import Device
from app.models import db
from flask_jwt_extended import jwt_required, get_jwt_identity

exam_bp = Blueprint('exam', __name__)

@exam_bp.route('/exams', methods=['GET'])
@jwt_required()
def get_exams():
    try:
        exams = Exam.query.all()
        exams_data = []

        for exam in exams:
            # Truy xuất thông tin về device từ cơ sở dữ liệu
            device = Device.query.get(exam.device_id)

            # Kiểm tra xem device có tồn tại hay không
            if not device:
                return jsonify({'message': 'Device not found'}), 404

            # Tạo thông tin về exam với thông tin về tên device
            exam_info = {
                'id': exam.id,
                'course_id': exam.course_id,
                'device_id': exam.device_id,
                'score': exam.score,
                'device_name': device.name,  # Thêm thông tin về tên device
                'created_at': exam.created_at.strftime("%Y-%m-%d %H:%M:%S"),  # Format ngày giờ
                'duration': str(exam.exam_duration)  # Chuyển đối timedelta thành chuỗi
            }

            exams_data.append(exam_info)

        return jsonify({'exams': exams_data})
    except Exception as e:
        return jsonify({'message': 'Error fetching exams' + str(e)}), 500

@exam_bp.route('/exams', methods=['POST'])
@jwt_required()
def create_exam():
    try:
        current_user = get_jwt_identity()
        if current_user['role'] == 'admin':
            data = request.get_json()
            
            new_exam = Exam(
                course_id=data['course_id'],
                device_id=data['device_id'],
                score=data['score'],
                user_id=data.get('user_id'),
                exam_duration=data.get('exam_duration'),
                create_at=data.get('create_at')
            )  # Thêm field user_id nếu cần
            db.session.add(new_exam)
            db.session.commit()

            return jsonify({'message': 'Exam created successfully'})
        else:
            return jsonify({'message': 'Unauthorized'}), 403
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error creating exam ' + str(e)}), 500

@exam_bp.route('/exams/<int:exam_id>', methods=['PUT'])
@jwt_required()
def update_exam(exam_id):
    try:
        current_user = get_jwt_identity()
        if current_user['role'] == 'admin':
            exam = Exam.query.get(exam_id)
            if exam:
                data = request.get_json()
                exam.course_id = data['course_id']
                exam.device_id = data['device_id']
                exam.score = data['score']
                exam.user_id = data.get('user_id')  # Thêm field user_id nếu cần
                exam.exam_duration = data.get('exam_duration'),
                exam.create_at = data.get('create_at')
                db.session.commit()
                return jsonify({'message': 'Exam updated successfully'})
            else:
                return jsonify({'message': 'Exam not found'}), 404
        else:
            return jsonify({'message': 'Unauthorized'}), 403
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error updating exam ' + str(e)}), 500

@exam_bp.route('/exams/<int:exam_id>', methods=['DELETE'])
@jwt_required()
def delete_exam(exam_id):
    try:
        current_user = get_jwt_identity()
        if current_user['role'] == 'admin':
            exam = Exam.query.get(exam_id)
            if exam:
                db.session.delete(exam)
                db.session.commit()
                return jsonify({'message': 'Exam deleted successfully'})
            else:
                return jsonify({'message': 'Exam not found'}), 404
        else:
            return jsonify({'message': 'Unauthorized'}), 403
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error deleting exam ' + str(e)}), 500
