from utils.db import db
from datetime import datetime

class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    chat_id = db.Column(db.Integer, db.ForeignKey("chat_sessions.id"), nullable=False)
    text = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
