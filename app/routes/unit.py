from flask import Blueprint, jsonify, request, redirect, session, url_for, flash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from app.models.unit import Unit
from app.models import db

unit_bp = Blueprint('unit', __name__)

@unit_bp.route('/units', methods=['GET'])
@jwt_required()
def get_units():
    current_user = get_jwt_identity()
    if current_user['role'] == 'admin':
        units = Unit.query.all()
        units_data = [{'id': unit.id, 'name': unit.name} for unit in units]
        return jsonify({'units': units_data})
    else:
        return jsonify({'message': 'Unauthorized'}), 403
@unit_bp.route('/units', methods=['POST'])
@jwt_required()
def create_unit():
    current_user = get_jwt_identity()
    if current_user['role'] == 'admin':
        data = request.get_json()
        if 'name' not in data or not data['name'].strip():
            return jsonify({'error': 'Invalid input data'}), 400
        new_unit = Unit(name=data['name'])
        try:
            db.session.add(new_unit)
            db.session.commit()
            return jsonify({'message': 'Unit created successfully'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'message': 'Unauthorized'}), 403
    
@unit_bp.route('/units/<int:unit_id>', methods=['PUT'])
@jwt_required()
def update_unit(unit_id):
    current_user = get_jwt_identity()
    if current_user['role'] == 'admin':
        unit = Unit.query.get(unit_id)
        if unit:
            data = request.get_json()
            unit.name = data['name']
            db.session.commit()
            return jsonify({'message': 'Unit updated successfully'})
        else:
            return jsonify({'message': 'Unit not found'}), 404
    else:
        return jsonify({'message': 'Unauthorized'}), 403
    
@unit_bp.route('/units/<int:unit_id>', methods=['DELETE'])
@jwt_required()
def delete_unit(unit_id):
    current_user = get_jwt_identity()
    if current_user['role'] == 'admin':
        unit = Unit.query.get(unit_id)
        if unit:
            db.session.delete(unit)
            db.session.commit()
            return jsonify({'message': 'Unit deleted successfully'})
        else:
            return jsonify({'message': 'Unit not found'}), 404
    else:
        return jsonify({'message': 'Unauthorized'}), 403

@unit_bp.route('/get-unit', methods=['POST'])
@jwt_required()
def get_unit_by_id():
    current_user = get_jwt_identity()
    data = request.get_json()
    unit_id = data.get('unit_id')
    unit = Unit.query.get(unit_id)
    if unit:
        unit_data = {'id': unit.id, 'name': unit.name} 
        return jsonify({'units': unit_data})
    else:
        return jsonify({'message': 'Unit not found'}), 404
