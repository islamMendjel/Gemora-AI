from utils.db import db
from datetime import datetime

class ChatSession(db.Model):
    __tablename__ = "chat_sessions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    messages = db.relationship("Message", backref="chat_session", lazy=True, cascade="all, delete")
