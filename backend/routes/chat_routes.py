from flask import Blueprint, request, jsonify
from utils.db import db
from utils.gemini_client import get_gemini_response
from models.message import Message
from flask_jwt_extended import jwt_required, get_jwt_identity

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/chat", methods=["POST"])
@jwt_required()
def chat():
    data = request.get_json()
    user_id = get_jwt_identity()
    user_message = data["message"]

    ai_response = get_gemini_response(user_message)

    message = Message(user_id=user_id, text=user_message, response=ai_response)
    db.session.add(message)
    db.session.commit()

    return jsonify({"response": ai_response})
