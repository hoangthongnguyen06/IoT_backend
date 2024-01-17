from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.device import Device
from app.models import db
from werkzeug.utils import secure_filename
import pandas as pd

device_bp = Blueprint('device', __name__)

@device_bp.route('/devices', methods=['GET'])
@jwt_required()
def get_devices():
    devices = Device.query.all()
    devices_data = [{'id': device.id, 'name': device.name, 'description': device.description, "ip_address": device.ip_address, 'status':device.status} for device in devices]
    return jsonify({'devices': devices_data})

@device_bp.route('/devices', methods=['POST'])
@jwt_required()
def create_device():
    current_user = get_jwt_identity()
    if current_user['role'] == 'admin':
        data = request.get_json()
        new_device = Device(name=data['name'], description=data['description'], ip_address=data['ip_address'], status=data['status'])
        db.session.add(new_device)
        db.session.commit()
        return jsonify({'message': 'Device created successfully'})
    else:
        return jsonify({'message': 'Unauthorized'}), 403

@device_bp.route('/upload_devices', methods=['POST'])
def upload_file():
    if 'devices_file' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    file = request.files['devices_file']

    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(filename)

        try:
            df = pd.read_excel(filename)

            for index, row in df.iterrows():
                new_device = Device(
                    name=row['name'],
                    description=row['description'],
                    ip_address=row['ip_address'],
                    status=row['status']
                )
                db.session.add(new_device)

            db.session.commit()

            return jsonify({'message': 'File uploaded and data added to the database successfully'})
        except Exception as e:
            return jsonify({'message': f'Error processing file: {str(e)}'}), 500
    else:
        return jsonify({'message': 'Invalid file format'}), 400

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
            device.status=data['status']
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
    
@device_bp.route('/get-device', methods=['POST'])
@jwt_required()
def get_device_by_id():
    data = request.get_json()

    device_id = data.get('device_id')
    if device_id is not None:
        device = Device.query.get(device_id)

        if device:
            device_data = {
                'id': device.id,
                'name': device.name,
                'description': device.description,
                'ip_address': device.ip_address,
                'status': device.status
            }
            return jsonify({'device': device_data})
        else:
            return jsonify({'message': 'Device not found'}), 404
    else:
        return jsonify({'message': 'Device ID is required in the request parameters'}), 400
    
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'xls', 'xlsx'}