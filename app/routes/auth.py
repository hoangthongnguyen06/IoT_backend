from flask import Blueprint, jsonify, request, flash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash
from app.models.user import User
from app.models import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    # if user and check_password_hash(user.password, password):
    if user and user.password==password:
        access_token = create_access_token(identity={'id': user.id, 'username': user.username, 'role': user.role})
        return jsonify(access_token=access_token, user_id=user.id, username=user.username, role=user.role)
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@auth_bp.route('/auth/logout', methods=['POST'])
@jwt_required()
def logout():
    return jsonify({'message': 'Logout successful'})

@auth_bp.route('/auth/current_user', methods=['GET'])
@jwt_required()
def get_current_user():
    current_user = get_jwt_identity()
    user = User.query.get(current_user['id'])
    return jsonify({'user_id': user.id, 'username': user.username, 'role': user.role})
