from flask import Blueprint, request, jsonify
from utils.db import db
from models.user import User
from utils.jwt_handler import generate_token

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    user = User(username=data["username"], email=data["email"])
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data["email"]).first()
    if user and user.check_password(data["password"]):
        token = generate_token(user.id)
        return jsonify({"access_token": token, "username": user.username}), 200
    return jsonify({"error": "Invalid credentials"}), 401
