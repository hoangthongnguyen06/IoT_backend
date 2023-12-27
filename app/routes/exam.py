from flask import Blueprint, jsonify, request
from app.models.exam import Exam, user_exam_association
from app.models.device import Device
from app.models.user import User
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
                'device_id': exam.device_id,
                'device_name': device.name,  # Thêm thông tin về tên device
                'created_at': exam.created_at.strftime("%Y-%m-%d %H:%M:%S"),  # Format ngày giờ
                'duration': str(exam.exam_duration)  # Chuyển đối timedelta thành chuỗi
            }
            exams_data.append(exam_info)

        return jsonify({'exams': exams_data})
    except Exception as e:
        return jsonify({'message': 'Error fetching exams' + str(e)}), 500

@exam_bp.route('/exams/<int:user_id>', methods=['GET'])
@jwt_required()
def get_exams_by_user(user_id):
    try:
        current_user = get_jwt_identity()
        if current_user['role'] == 'user':
            user = User.query.get(user_id)
            if user:
                # Lấy danh sách bài thi của người dùng từ bảng liên kết
                user_exams = db.session.query(Exam, user_exam_association.c.score).join(
                    user_exam_association,
                    user_exam_association.c.exam_id == Exam.id
                ).filter(
                    user_exam_association.c.user_id == user_id
                ).all()
                
                exams_data = []
                for exam, score in user_exams:
                    # Truy xuất thông tin về device từ cơ sở dữ liệu
                    device = Device.query.get(exam.device_id)

                    # Kiểm tra xem device có tồn tại hay không
                    if not device:
                        return jsonify({'message': 'Device not found'}), 404

                    # Tạo thông tin về exam với thông tin về tên device
                    exam_info = {
                        'id': exam.id,
                        'device_id': exam.device_id,
                        'device_name': device.name,  # Thêm thông tin về tên device
                        'created_at': exam.created_at.strftime("%Y-%m-%d %H:%M:%S"),  # Format ngày giờ
                        'duration': str(exam.exam_duration),  # Chuyển đối timedelta thành chuỗi
                        'score': score
                    }
                    exams_data.append(exam_info)

                return jsonify({'user_exams': exams_data})
            else:
                return jsonify({'message': 'User not found'}), 404
        else:
            return jsonify({'message': 'Unauthorized'}), 403
    except Exception as e:
        return jsonify({'message': 'Error fetching exams by user: ' + str(e)}), 500

@exam_bp.route('/exams/<int:exam_id>/update-score', methods=['POST'])
@jwt_required()
def update_user_exam_score(exam_id):
    try:
        current_user = get_jwt_identity()

        if current_user['role'] == 'admin':
            data = request.get_json()
            user_id = data.get('user_id')
            score = data.get('score')

            # Kiểm tra sự tồn tại của Exam và User
            exam = Exam.query.get(exam_id)
            user = User.query.get(user_id)

            if exam and user:
                # Kiểm tra xem user đã tham gia kỳ thi này chưa
                user_exam_association_record = db.session.query(user_exam_association).filter(
                    (user_exam_association.c.user_id == user_id) &
                    (user_exam_association.c.exam_id == exam_id)
                ).first()

                if user_exam_association_record:
                    # Cập nhật điểm trong bảng liên kết
                    user_exam_association_record = db.session.query(user_exam_association).filter(
                        (user_exam_association.c.user_id == user_id) &
                        (user_exam_association.c.exam_id == exam_id)
                    ).update({"score": score})

                    db.session.commit()
                    return jsonify({'message': 'Score updated successfully'})
                else:
                    return jsonify({'message': 'User has not participated in this exam'}), 400
            else:
                return jsonify({'message': 'Exam or User not found'}), 404
        else:
            return jsonify({'message': 'Unauthorized'}), 403
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error updating score: {str(e)}'}), 500

@exam_bp.route('/exams', methods=['POST'])
@jwt_required()
def create_exam():
    try:
        current_user = get_jwt_identity()
        if current_user['role'] == 'admin':
            data = request.get_json()
            
            new_exam = Exam(
                device_id=data['device_id'],
                exam_duration=data.get('exam_duration'),
                created_at=data.get('create_at')
            ) 
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
                exam.device_id = data['device_id']
                exam.exam_duration = data.get('exam_duration'),
                exam.created_at = data.get('created_at')
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
