from flask import Blueprint, request, jsonify
from utils.db import db
from models.user import User
from utils.jwt_handler import generate_access_token, generate_refresh_token
from flask_jwt_extended import jwt_required, get_jwt_identity, jwt_required, get_jwt_identity, decode_token

auth_bp = Blueprint("auth", __name__)

def simple_valid_email(email: str) -> bool:
    import re
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))

# --------------------------
# 🧩 Signup Route
# --------------------------
@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json() or {}
    username = (data.get("username") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not username or not email or not password:
        return jsonify({"error": "username, email, and password are required"}), 400
    if not simple_valid_email(email):
        return jsonify({"error": "invalid email format"}), 400
    if len(password) < 6:
        return jsonify({"error": "password must be at least 6 characters"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 400

    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201

# --------------------------
# 🔐 Login Route (returns access + refresh)
# --------------------------
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({"error": "email and password are required"}), 400

    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        access = generate_access_token(user.id)
        refresh = generate_refresh_token(user.id)
        return jsonify({"access_token": access, "refresh_token": refresh, "username": user.username}), 200

    return jsonify({"error": "Invalid credentials"}), 401

# --------------------------
# 🔁 Refresh endpoint
# --------------------------
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token

@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    new_access = create_access_token(identity=identity)
    return jsonify({"access_token": new_access}), 200

# --------------------------
# ✅ Verify Token Route
# --------------------------
@auth_bp.route("/verify", methods=["GET"])
@jwt_required()
def verify():
    user_id = get_jwt_identity()
    return jsonify({"msg": "Token is valid", "user_id": user_id}), 200