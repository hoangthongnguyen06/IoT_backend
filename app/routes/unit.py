from flask import Blueprint, jsonify, request, redirect, session, url_for, flash
from app.models.unit import Unit
from app.models import db

unit_bp = Blueprint('unit', __name__)

@unit_bp.route('/units', methods=['GET'])
def get_units():
    units = Unit.query.all()
    units_data = [{'id': unit.id, 'name': unit.name} for unit in units]
    return jsonify({'units': units_data})

@unit_bp.route('/units', methods=['POST'])
def create_unit():
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

@unit_bp.route('/units/<int:unit_id>', methods=['PUT'])
def update_unit(unit_id):
    unit = Unit.query.get(unit_id)
    if unit:
        data = request.get_json()
        unit.name = data['name']
        db.session.commit()
        return jsonify({'message': 'Unit updated successfully'})
    else:
        return jsonify({'message': 'Unit not found'}), 404

@unit_bp.route('/units/<int:unit_id>', methods=['DELETE'])
def delete_unit(unit_id):
    unit = Unit.query.get(unit_id)
    if unit:
        db.session.delete(unit)
        db.session.commit()
        return jsonify({'message': 'Unit deleted successfully'})
    else:
        return jsonify({'message': 'Unit not found'}), 404

def create_unit_blueprint():
    return unit_bp
