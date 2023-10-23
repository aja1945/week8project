from flask import Blueprint, request, jsonify
from models import db, User
from flask_jwt_extended import create_access_token

user_bp = Blueprint('user', __name__)

@user_bp.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()

    if User.query.filter_by(username=data['username']).first() is not None:
        return jsonify({'message': 'Username already exists'}), 400

    if User.query.filter_by(email=data['email']).first() is not None:
        return jsonify({'message': 'Email already in use'}), 400

    new_user = User(username=data['username'], email=data['email'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

@user_bp.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()

    if user is None or not user.check_password(data['password']):
        return jsonify({'message': 'Invalid username or password'}), 401

    access_token = create_access_token(identity=user.username)
    return jsonify(access_token=access_token), 200

from users.user import user_bp

app.register_blueprint(user_bp, url_prefix='/user')

lass(db.Model)
def check_password(self, password):
        return password == self.password