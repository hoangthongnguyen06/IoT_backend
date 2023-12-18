from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from app.models import db
from werkzeug.security import generate_password_hash, check_password_hash

user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    current_user = get_jwt_identity()
    if current_user['role'] == 'admin':
        users = User.query.all()
        users_data = [{'id': user.id, 'username': user.username, 'email': user.email, 'role': user.role} for user in users]
        return jsonify({'users': users_data})
    else:
        return jsonify({'message': 'Unauthorized'}), 403

@user_bp.route('/users', methods=['POST'])
@jwt_required()
def create_user():
    current_user = get_jwt_identity()
    if current_user['role'] == 'admin':
        data = request.get_json()
        new_user = User(username=data['username'], email=data['email'], password=generate_password_hash(data['password'], method='sha256'))
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'})
    else:
        return jsonify({'message': 'Unauthorized'}), 403

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    current_user = get_jwt_identity()
    if current_user['role'] == 'admin':
        user = User.query.get(user_id)
        if user:
            data = request.get_json()
            user.username = data['username']
            user.email = data['email']
            user.password = generate_password_hash(data['password'], method='sha256')
            db.session.commit()
            return jsonify({'message': 'User updated successfully'})
        else:
            return jsonify({'message': 'User not found'}), 404
    else:
        return jsonify({'message': 'Unauthorized'}), 403

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    current_user = get_jwt_identity()
    if current_user['role'] == 'admin':
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify({'message': 'User deleted successfully'})
        else:
            return jsonify({'message': 'User not found'}), 404
    else:
        return jsonify({'message': 'Unauthorized'}), 403
