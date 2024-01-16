from flask import Blueprint, jsonify, request
from app.models.exam import Exam, user_exam_association
from app.models.device import Device
from app.models.user import User
from flask import send_from_directory
from app.models import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from flask import Blueprint, request, jsonify, current_app
import os
from datetime import datetime

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
                'device_status': device.status,
                'created_at': exam.created_at.strftime("%Y-%m-%d %H:%M:%S"),  # Format ngày giờ
                'duration': str(exam.exam_duration)  # Chuyển đối timedelta thành chuỗi
            }
            exams_data.append(exam_info)

        return jsonify({'exams': exams_data})
    except Exception as e:
        return jsonify({'message': 'Error fetching exams' + str(e)}), 500

@exam_bp.route('/my-exams', methods=['GET'])
@jwt_required()
def get_exams_by_user():
    try:
        current_user = get_jwt_identity()
        user_id = current_user['id']
        if current_user['role'] == 'user':
            user = User.query.get(user_id)
            if user:
                # Lấy danh sách bài thi của người dùng từ bảng liên kết
                user_exams = db.session.query(Exam, user_exam_association.c.score, user_exam_association.c.exam_answer_path).join(
                    user_exam_association,
                    user_exam_association.c.exam_id == Exam.id
                ).filter(
                    user_exam_association.c.user_id == user_id
                ).all()
                
                exams_data = []
                for exam, score, exam_answer_path in user_exams:
                    # Truy xuất thông tin về device từ cơ sở dữ liệu
                    device = Device.query.get(exam.device_id)

                    # Kiểm tra xem device có tồn tại hay không
                    if not device:
                        return jsonify({'message': 'Device not found'}), 404
                    if exam_answer_path != "null":
                        exam_answer_path = "Đã nộp bài thi"
                    else: exam_answer_path="Chưa nộp bài thi"

                    # Tạo thông tin về exam với thông tin về tên device
                    exam_info = {
                        'id': exam.id,
                        'device_id': exam.device_id,
                        'device_name': device.name,
                        'device_IP': device.ip_address,  # Thêm thông tin về tên device
                        'created_at': exam.created_at.strftime("%Y-%m-%d %H:%M:%S"),  # Format ngày giờ
                        'duration': str(exam.exam_duration),  # Chuyển đối timedelta thành chuỗi
                        'score': score,
                        'exam_id': exam.id,
                        'exam_answer_path':exam_answer_path
                    }
                    exams_data.append(exam_info)

                return jsonify({'user_exams': exams_data})
            else:
                return jsonify({'message': 'User not found'}), 404
        else:
            return jsonify({'message': 'Unauthorized'}), 403
    except Exception as e:
        return jsonify({'message': 'Error fetching exams by user: ' + str(e)}), 500

@exam_bp.route('/exams/update-score', methods=['POST'])
@jwt_required()
def update_user_exam_score():
    try:
        current_user = get_jwt_identity()

        if current_user['role'] == 'admin':
            data = request.get_json()
            user_id = data.get('user_id')
            score = data.get('score')

            # Kiểm tra sự tồn tại của User
            user = User.query.get(user_id)

            if user:
                # Kiểm tra xem user đã tham gia kỳ thi nào chưa
                user_exam_association_record = db.session.query(user_exam_association).filter(
                    user_exam_association.c.user_id == user_id
                ).first()

                if user_exam_association_record:
                    exam_id = user_exam_association_record.exam_id

                    # Cập nhật điểm trong bảng liên kết
                    db.session.query(user_exam_association).filter(
                        (user_exam_association.c.user_id == user_id) &
                        (user_exam_association.c.exam_id == exam_id)
                    ).update({"score": score})

                    db.session.commit()
                    return jsonify({'message': 'Score updated successfully'})
                else:
                    return jsonify({'message': 'User has not participated in any exam'}), 400
            else:
                return jsonify({'message': 'User not found'}), 404
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



# @exam_bp.route('/upload_exam_answer', methods=['POST'])
# @jwt_required()
# def upload_exam():
#     current_user = get_jwt_identity()
    
#     # Kiểm tra xem người dùng có quyền upload bài thi hay không
#     if current_user['role'] != 'user':
#         return jsonify({'message': 'Unauthorized'}), 403

#     exam_id = request.form['exam_id']
#     exam = Exam.query.get(exam_id)
    
#     # Kiểm tra xem bài thi có tồn tại hay không
#     if not exam:
#         return jsonify({'message': 'Exam not found'}), 404

#     # Lấy nội dung bài làm từ request
#     exam_answer_file = request.files['exam_answer_file']

#     # Kiểm tra định dạng file
#     if exam_answer_file and allowed_file(exam_answer_file.filename):
#         # Tạo một tên an toàn cho file
#         filename = secure_filename(exam_answer_file.filename)
#         user_course_id = db.session.query(User.course_id).filter_by(id=current_user['id']).scalar()
#         # Thư mục lưu trữ file (tương đối)
#         upload_folder = os.path.join(current_app.root_path, 'exam_answers', str(user_course_id))

#         # Tạo thư mục nếu nó không tồn tại
#         if not os.path.exists(upload_folder):
#             os.makedirs(upload_folder)

#         # Lưu file vào thư mục được cấu hình
#         exam_path = os.path.join(str(user_course_id), filename)
#         exam_answer_file.save(os.path.join(upload_folder, filename))

#         # Lưu đường dẫn tương đối của file vào cơ sở dữ liệu
#         current_user_exam_association = user_exam_association.insert().values(
#             user_id=current_user['id'],
#             exam_id=exam_id,
#             exam_answer_path=exam_path
#         )
#         db.session.execute(current_user_exam_association)
#         db.session.commit()

#         return jsonify({'message': 'Exam uploaded successfully'})
#     else:
#         return jsonify({'message': 'Invalid file format'}), 400

@exam_bp.route('/upload_exam_answer', methods=['POST'])
@jwt_required()
def upload_exam():
    current_user = get_jwt_identity()

    # Kiểm tra xem người dùng có quyền upload bài thi hay không
    if current_user['role'] != 'user':
        return jsonify({'message': 'Unauthorized'}), 403

    exam_id = request.form['exam_id']
    exam = Exam.query.get(exam_id)

    # Kiểm tra xem bài thi có tồn tại hay không
    if not exam:
        return jsonify({'message': 'Exam not found'}), 404

    # Lấy nội dung bài làm từ request
    exam_answer_file = request.files['exam_answer_file']

    # Kiểm tra định dạng file
    if exam_answer_file and allowed_file(exam_answer_file.filename):
        # Tạo một tên an toàn cho file
        filename = secure_filename(exam_answer_file.filename)
        user_course_id = db.session.query(User.course_id).filter_by(id=current_user['id']).scalar()

        # Thư mục lưu trữ file (tương đối)
        upload_folder = os.path.join(current_app.root_path, 'exam_answers', str(user_course_id))

        # Tạo thư mục nếu nó không tồn tại
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        # Đường dẫn đầy đủ của file
        full_path = os.path.join(upload_folder, filename)

        # Kiểm tra xem file đã tồn tại chưa
        if os.path.exists(full_path):
            # Nếu tồn tại, bạn có thể xử lý logic replace file ở đây
            os.remove(full_path)  # Xóa file cũ để thay thế bằng file mới
            # Cập nhật đường dẫn trong cơ sở dữ liệu
            exam_answer_file.save(full_path)    
            exam_path = os.path.join(str(user_course_id), filename)
            current_user_exam_association = user_exam_association.update().values(
                exam_answer_path=exam_path
            ).where(
                user_exam_association.c.user_id == current_user['id'] and user_exam_association.c.exam_id == exam_id
            )
            db.session.execute(current_user_exam_association)
            db.session.commit()
            return jsonify({'message': 'Exam replaced successfully'})
        else:
            # Nếu chưa tồn tại, lưu file như bình thường
            exam_path = os.path.join(str(user_course_id), filename)
            exam_answer_file.save(full_path)

            # Lưu đường dẫn tương đối của file vào cơ sở dữ liệu
            current_user_exam_association = user_exam_association.update().values(
        exam_answer_path=exam_path
    ).where(
        user_exam_association.c.user_id == current_user['id'] and user_exam_association.c.exam_id == exam_id
    )
            db.session.execute(current_user_exam_association)
            db.session.commit()

            return jsonify({'message': 'Exam uploaded successfully'})
    else:
        return jsonify({'message': 'Invalid file format'}), 400

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'doc', 'docx'}

@exam_bp.route('/download-exam', methods=['POST'])
@jwt_required()
def download_exam():
    current_user = get_jwt_identity()

    # Kiểm tra xem người dùng có quyền admin hay không
    if current_user['role'] != 'admin':
        return jsonify({'message': 'Unauthorized'}), 403
    data = request.get_json()
    user_id = data.get('user_id')

    # Lấy đường dẫn tương đối của bài làm từ cơ sở dữ liệu
    user_exam_info = db.session.query(user_exam_association).\
        filter(user_exam_association.c.user_id == user_id).first()

    if user_exam_info:
        exam_id = user_exam_info.exam_id
        
        # Lấy đường dẫn đầy đủ từ bảng user_exam_association
        user_exam_path = user_exam_info.exam_answer_path

        # Phần còn lại của mã không đổi
        try:
            course_id, filename = user_exam_path.split('\\')    
        except:
            course_id, filename = user_exam_path.split('/')

        directory = os.path.join(current_app.root_path, 'exam_answers', str(course_id))
        
        # Trả về file cho admin tải xuống
        return send_from_directory(directory, filename, as_attachment=True)
    else:
        return jsonify({'message': 'User exam not found'}), 404