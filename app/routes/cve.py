
from flask import Blueprint, jsonify, request, redirect, session, url_for, flash
from flask import Blueprint, jsonify, request, flash, redirect, url_for, session
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from app.models.cve import CVE
from app.models import db

cve_bp = Blueprint('cve', __name__)


@cve_bp.route('/cves', methods=['GET'])
@jwt_required()
def get_cves():
    cves = CVE.query.all()
    cves_data = [{'id': cve.id, 'description': cve.description, 'name': cve.name} for cve in cves]
    return jsonify({'cves': cves_data})

@cve_bp.route('/cves', methods=['POST'])
@jwt_required()
def create_cve():
    current_user = get_jwt_identity()
    if current_user['role'] == 'admin':
        data = request.get_json()
        new_cve = CVE(description=data['description'], name=data['name'])
        db.session.add(new_cve)
        db.session.commit()
        return jsonify({'message': 'CVE created successfully'})

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


