from flask import Blueprint, request, jsonify
from utils.db import db
# from backend.models.chat_session import Conversation
from flask_jwt_extended import jwt_required, get_jwt_identity

conv_bp = Blueprint("conversations", __name__)

@conv_bp.route("/", methods=["GET"])
@jwt_required()
def list_conversations():
    uid = get_jwt_identity()
    convs = Conversation.query.filter_by(user_id=uid).order_by(Conversation.updated_at.desc()).all()
    return jsonify([
        {"id": c.id, "title": c.title or "New chat", "updated_at": c.updated_at.strftime("%Y-%m-%d %H:%M:%S")}
        for c in convs
    ]), 200

@conv_bp.route("/", methods=["POST"])
@jwt_required()
def create_conversation():
    uid = get_jwt_identity()
    data = request.get_json() or {}
    title = data.get("title", "New Chat")
    conv = Conversation(user_id=uid, title=title)
    db.session.add(conv)
    db.session.commit()
    return jsonify({"id": conv.id, "title": conv.title}), 201