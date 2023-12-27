from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.device import Device
from app.models import db

device_bp = Blueprint('device', __name__)

@device_bp.route('/devices', methods=['GET'])
@jwt_required()
def get_devices():
    devices = Device.query.all()
    devices_data = [{'id': device.id, 'name': device.name, 'description': device.description, "ip_address": device.ip_address} for device in devices]
    return jsonify({'devices': devices_data})

@device_bp.route('/devices', methods=['POST'])
@jwt_required()
def create_device():
    current_user = get_jwt_identity()
    if current_user['role'] == 'admin':
        data = request.get_json()
        new_device = Device(name=data['name'], description=data['description'], ip_address=data['ip_address'])
        db.session.add(new_device)
        db.session.commit()
        return jsonify({'message': 'Device created successfully'})
    else:
        return jsonify({'message': 'Unauthorized'}), 403
@device_bp.route('/devices/<int:device_id>', methods=['PUT'])
@jwt_required()
def update_device(device_id):
    current_user = get_jwt_identity()
    if current_user['role'] == 'admin':
        device = Device.query.get(device_id)
        if device:
            data = request.get_json()
            device.name = data['name']
            device.description = data['description']
            device.ip_address=data['ip_address']
            db.session.commit()
            return jsonify({'message': 'Device updated successfully'})
        else:
            return jsonify({'message': 'Device not found'}), 404
    else:
        return jsonify({'message': 'Unauthorized'}), 403
@device_bp.route('/devices/<int:device_id>', methods=['DELETE'])
@jwt_required()
def delete_device(device_id):
    current_user = get_jwt_identity()
    if current_user['role'] == 'admin':
        device = Device.query.get(device_id)
        if device:
            db.session.delete(device)
            db.session.commit()
            return jsonify({'message': 'Device deleted successfully'})
        else:
            return jsonify({'message': 'Device not found'}), 404
    else:
            return jsonify({'message': 'Unauthorized'}), 403