from flask import Blueprint, jsonify, request
from app.models.cve import CVE
from app.models import db

cve_bp = Blueprint('cve', __name__)

@cve_bp.route('/cves', methods=['GET'])
def get_cves():
    cves = CVE.query.all()
    cves_data = [{'id': cve.id, 'description': cve.description, 'exploit_path': cve.exploit_path} for cve in cves]
    return jsonify({'cves': cves_data})

@cve_bp.route('/cves', methods=['POST'])
def create_cve():
    data = request.get_json()
    new_cve = CVE(description=data['description'], exploit_path=data['exploit_path'])
    db.session.add(new_cve)
    db.session.commit()
    return jsonify({'message': 'CVE created successfully'})

@cve_bp.route('/cves/<int:cve_id>', methods=['PUT'])
def update_cve(cve_id):
    cve = CVE.query.get(cve_id)
    if cve:
        data = request.get_json()
        cve.description = data['description']
        cve.exploit_path = data['exploit_path']
        db.session.commit()
        return jsonify({'message': 'CVE updated successfully'})
    else:
        return jsonify({'message': 'CVE not found'}), 404

@cve_bp.route('/cves/<int:cve_id>', methods=['DELETE'])
def delete_cve(cve_id):
    cve = CVE.query.get(cve_id)
    if cve:
        db.session.delete(cve)
        db.session.commit()
        return jsonify({'message': 'CVE deleted successfully'})
    else:
        return jsonify({'message': 'CVE not found'}), 404
