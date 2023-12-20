from flask import Blueprint, jsonify, request, redirect, session, url_for, flash
from app.models.device import Device
from app.models import db

device_bp = Blueprint('device', __name__)

@device_bp.route('/devices', methods=['GET'])
def get_devices():
    devices = Device.query.all()
    devices_data = [{'id': device.id, 'name': device.name, 'description': device.description, 'cve_id': device.cve_id} for device in devices]
    return jsonify({'devices': devices_data})

@device_bp.route('/devices', methods=['POST'])
def create_device():
    data = request.get_json()
    new_device = Device(name=data['name'], description=data['description'], cve_id=data['cve_id'])
    db.session.add(new_device)
    db.session.commit()
    return jsonify({'message': 'Device created successfully'})

@device_bp.route('/devices/<int:device_id>', methods=['PUT'])
def update_device(device_id):
    device = Device.query.get(device_id)
    if device:
        data = request.get_json()
        device.name = data['name']
        device.description = data['description']
        device.cve_id = data['cve_id']
        db.session.commit()
        return jsonify({'message': 'Device updated successfully'})
    else:
        return jsonify({'message': 'Device not found'}), 404

@device_bp.route('/devices/<int:device_id>', methods=['DELETE'])
def delete_device(device_id):
    device = Device.query.get(device_id)
    if device:
        db.session.delete(device)
        db.session.commit()
        return jsonify({'message': 'Device deleted successfully'})
    else:
        return jsonify({'message': 'Device not found'}), 404

def create_device_blueprint():
    return device_bp
