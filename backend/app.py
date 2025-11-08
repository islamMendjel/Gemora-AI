from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from utils.db import db
from config import Config
from routes.auth_routes import auth_bp
from routes.chat_routes import chat_bp

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
db.init_app(app)
jwt = JWTManager(app)

with app.app_context():
    db.create_all()

app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(chat_bp, url_prefix="/api/chat")

if __name__ == "__main__":
    app.run(debug=True)
