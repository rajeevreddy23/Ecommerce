from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from flask_bcrypt import Bcrypt
from database import get_db
from models import User

auth_bp = Blueprint('auth', __name__)
bcrypt = Bcrypt()

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password') or not data.get('name'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    db = get_db()
    
    if User.find_by_email(db, data['email']):
        return jsonify({'error': 'Email already exists'}), 409
    
    try:
        user_id = User.create(db, data['email'], data['password'], data['name'])
        return jsonify({'message': 'User created successfully', 'user_id': str(user_id)}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing email or password'}), 400
    
    db = get_db()
    user = User.find_by_email(db, data['email'])
    
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    if not bcrypt.check_password_hash(user['password'], data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    access_token = create_access_token(identity=str(user['_id']))
    return jsonify({
        'access_token': access_token,
        'user': {
            'id': str(user['_id']),
            'email': user['email'],
            'name': user['name']
        }
    }), 200

@auth_bp.route('/verify', methods=['GET'])
def verify():
    from flask_jwt_extended import jwt_required, get_jwt_identity
    
    @jwt_required()
    def verify_token():
        user_id = get_jwt_identity()
        db = get_db()
        user = User.find_by_id(db, user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'user': {
                'id': str(user['_id']),
                'email': user['email'],
                'name': user['name']
            }
        }), 200
    
    return verify_token()
