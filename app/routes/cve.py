
from flask import Blueprint, jsonify, request
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.cve import CVE
from app.models import db

cve_bp = Blueprint('cve', __name__)


@cve_bp.route('/cves', methods=['GET'])
@jwt_required()
def get_cves():
    cves = CVE.query.all()
    cves_data = [{'id': cve.id, 'description': cve.description, 'name': cve.name, 'severity': cve.severity, "score":cve.score} for cve in cves]
    return jsonify({'cves': cves_data})

@cve_bp.route('/cves', methods=['POST'])
@jwt_required()
def create_cve():
    current_user = get_jwt_identity()
    if current_user['role'] == 'admin':
        data = request.get_json()
        new_cve = CVE(description=data['description'], name=data['name'], score=data['score'])  # Thêm điểm vào khi tạo mới
        db.session.add(new_cve)
        db.session.commit()
        return jsonify({'message': 'CVE created successfully'})
    else:
        return jsonify({'message': 'Unauthorized'})
@cve_bp.route('/cves/<int:cve_id>', methods=['PUT'])
@jwt_required()
def update_cve(cve_id):
    cve = CVE.query.get(cve_id)
    current_user = get_jwt_identity()
    if current_user['role'] == 'admin':
        if cve:
            data = request.get_json()
            cve.description = data['description']
            cve.name = data['name']
            cve.score = data['score']  # Cập nhật điểm
            cve.calculate_severity()  # Tính toán lại mức độ
            db.session.commit()
            return jsonify({'message': 'CVE updated successfully'})
        else:
            return jsonify({'message': 'CVE not found'}), 404

@cve_bp.route('/cves/<int:cve_id>', methods=['DELETE'])
@jwt_required()
def delete_cve(cve_id):
    cve = CVE.query.get(cve_id)
    current_user = get_jwt_identity()
    if current_user['role'] == 'admin':
        if cve:
            db.session.delete(cve)
            db.session.commit()
            return jsonify({'message': 'CVE deleted successfully'})
        else:
            return jsonify({'message': 'CVE not found'}), 404

@cve_bp.route('/cve-info', methods=['POST'])
@jwt_required()
def get_cve_by_id():
    data = request.get_json()
    cve_id = data['cve_id']
    cve = CVE.query.get(cve_id)

    if cve:
        cve_data = {
            'id': cve.id,
            'description': cve.description,
            'name': cve.name,
            'severity': cve.severity,
            'score':cve.score
            # Thêm các trường khác nếu cần
        }
        return jsonify({'cve': cve_data})
    else:
        return jsonify({'message': 'CVE not found'}), 404