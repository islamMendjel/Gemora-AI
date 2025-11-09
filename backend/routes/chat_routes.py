from flask import Blueprint, request, jsonify
from utils.db import db
from utils.gemini_client import get_gemini_response
from models.messages import Message
from models.chat_session import ChatSession
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.logger import logger
from sqlalchemy.exc import SQLAlchemyError

chat_bp = Blueprint("chat", __name__)

# -------------------------
# 🆕 Create new chat
# -------------------------
@chat_bp.route("/new", methods=["POST"])
@jwt_required()
def new_chat():
    try:
        user_id = get_jwt_identity()
        data = request.get_json() or {}
        first_message = (data.get("message") or "").strip()

        if not first_message:
            return jsonify({"error": "Message is required"}), 400

        ai_title_prompt = f"Generate a short 3-5 word title for this chat topic: {first_message}"
        try:
            raw_title = get_gemini_response(ai_title_prompt)
            title = (raw_title or "Untitled Chat").splitlines()[0][:60]
        except Exception as e:
            logger.warning(f"Failed to generate title: {e}")
            title = "Untitled Chat"

        chat = ChatSession(user_id=user_id, title=title)
        db.session.add(chat)
        db.session.commit()

        try:
            ai_response = get_gemini_response(first_message)
        except Exception as e:
            logger.error(f"Gemini failed to respond: {e}", exc_info=True)
            ai_response = "AI Error generating response."

        message = Message(
            user_id=user_id,
            chat_id=chat.id,
            text=first_message,
            response=ai_response
        )
        db.session.add(message)
        db.session.commit()

        return jsonify({
            "chat_id": chat.id,
            "title": chat.title,
            "response": ai_response
        }), 201

    except SQLAlchemyError as db_err:
        db.session.rollback()
        logger.error(f"DB error in /new: {db_err}", exc_info=True)
        return jsonify({"error": "Database error", "details": str(db_err)}), 500

    except Exception as e:
        logger.error(f"Unhandled /new error: {e}", exc_info=True)
        return jsonify({"error": "Server error", "details": str(e)}), 500


# -------------------------
# 💬 Continue an existing chat
# -------------------------
@chat_bp.route("/send", methods=["POST"])
@jwt_required()
def send_message():
    try:
        data = request.get_json() or {}
        user_id = get_jwt_identity()
        chat_id = data.get("chat_id")
        message_text = (data.get("message") or "").strip()

        if not chat_id or not message_text:
            return jsonify({"error": "chat_id and message are required"}), 400

        chat = ChatSession.query.filter_by(id=chat_id, user_id=user_id).first()
        if not chat:
            return jsonify({"error": "Chat not found"}), 404

        try:
            ai_response = get_gemini_response(message_text)
        except Exception as e:
            logger.error(f"Gemini failed during send: {e}", exc_info=True)
            ai_response = "AI Error generating response."

        msg = Message(
            user_id=user_id,
            chat_id=chat.id,
            text=message_text,
            response=ai_response
        )
        db.session.add(msg)
        db.session.commit()

        return jsonify({
            "response": ai_response,
            "chat_id": chat.id
        }), 200

    except SQLAlchemyError as db_err:
        db.session.rollback()
        logger.error(f"DB error in /send: {db_err}", exc_info=True)
        return jsonify({"error": "Database error", "details": str(db_err)}), 500

    except Exception as e:
        logger.error(f"Unhandled /send error: {e}", exc_info=True)
        return jsonify({"error": "Server error", "details": str(e)}), 500

# -------------------------
# 🧠 chat history list
# -------------------------
@chat_bp.route("/list", methods=["GET"])
@jwt_required()
def list_chats():
    user_id = get_jwt_identity()
    chats = (
        db.session.query(ChatSession)
        .join(Message, ChatSession.id == Message.chat_id)
        .filter(ChatSession.user_id == user_id)
        .group_by(ChatSession.id)
        .order_by(ChatSession.created_at.desc())
        .all()
    )

    return jsonify([
        {
            "id": c.id,
            "title": c.title or "Untitled Chat",
            "created_at": c.created_at.strftime("%Y-%m-%d %H:%M")
        } for c in chats
    ]), 200



# -------------------------
# 🧠 Get chat history
# -------------------------
@chat_bp.route("/<int:chat_id>/history", methods=["GET"])
@jwt_required()
def chat_history(chat_id):
    user_id = get_jwt_identity()
    chat = ChatSession.query.filter_by(id=chat_id, user_id=user_id).first()
    if not chat:
        return jsonify({"error": "Chat not found"}), 404

    messages = (
        Message.query
        .filter_by(chat_id=chat.id)
        .order_by(Message.timestamp.asc())
        .all()
    )

    result = []
    for m in messages:
        result.append({"role": "user", "text": m.text, "timestamp": m.timestamp.strftime("%H:%M")})
        result.append({"role": "assistant", "text": m.response, "timestamp": m.timestamp.strftime("%H:%M")})

    return jsonify({
        "chat_id": chat.id,
        "title": chat.title,
        "messages": result
    }), 200

# -------------------------
# ❌ Delete a chat (and its messages)
# -------------------------
@chat_bp.route("/<int:chat_id>/delete", methods=["DELETE"])
@jwt_required()
def delete_chat(chat_id):
    user_id = get_jwt_identity()
    chat = ChatSession.query.filter_by(id=chat_id, user_id=user_id).first()

    if not chat:
        return jsonify({"error": "Chat not found"}), 404

    try:
        db.session.delete(chat)
        db.session.commit()
        return jsonify({"message": "Chat deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to delete chat", "details": str(e)}), 500
