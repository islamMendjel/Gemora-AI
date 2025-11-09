import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from sqlalchemy import text
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from utils.db import db
from config import Config
from utils.logger import logger
from utils.limiter_config import limiter
from flask_talisman import Talisman

# ---------------------------------
# 🧠 App Setup
# ---------------------------------
app = Flask(__name__)
app.config.from_object(Config)

app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["DEBUG"] = True


# Security headers
Talisman(app)

# CORS whitelist
if Config.CORS_ORIGINS:
    CORS(app, origins=Config.CORS_ORIGINS)
else:
    CORS(app)

db.init_app(app)
jwt = JWTManager(app)

# Bind limiter to the Flask app (redis storage configured in limiter_config)
limiter.init_app(app)

# Import routes AFTER initializing extensions (avoids circular imports)
from routes.auth_routes import auth_bp
from routes.chat_routes import chat_bp
from models import User, Message

# ---------------------------------
# 🪵 Logging
# ---------------------------------
@app.before_request
def log_request_info():
    logger.info(f"{request.remote_addr} -> Request: {request.method} {request.path}")

@app.after_request
def log_response_info(response):
    logger.info(f"{request.remote_addr} -> Response: {response.status}")
    return response

# ---------------------------------
# 🧩 Error Handlers
# ---------------------------------
@app.errorhandler(400)
def bad_request(e):
    return jsonify({"error": "Bad Request", "message": str(e)}), 400

@app.errorhandler(401)
def unauthorized(e):
    return jsonify({"error": "Unauthorized", "message": str(e)}), 401

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not Found"}), 404

@app.errorhandler(429)
def rate_limited(e):
    return jsonify({"error": "Too Many Requests", "message": str(e)}), 429

@app.errorhandler(500)
def internal_error(e):
    logger.error("Internal server error", exc_info=True)
    return jsonify({"error": "Internal Server Error", "message": str(e)}), 500

# @app.errorhandler(Exception)
# def handle_exception(e):
#     logger.error(f"Unhandled Exception: {e}", exc_info=True)
#     return jsonify({"error": "Unexpected Server Error"}), 500


# ---------------------------------
# 🗄️ Database Initialization
# ---------------------------------
with app.app_context():
    db.create_all()

# ---------------------------------
# 🧩 Blueprints
# ---------------------------------
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(chat_bp, url_prefix="/api/chat")

# ---------------------------------
# ❤️ Health Check
# ---------------------------------
@app.route("/api/health")
def health():
    try:
        db.session.execute(text("SELECT 1"))
        db_ok = True
    except Exception as exc:
        logger.error("DB health check failed", exc_info=True)
        db_ok = False
    return jsonify({
        "status": "ok",
        "database": db_ok,
        "ai_connected": True
    }), 200


# ---------------------------------
# 🚀 Run Server
# ---------------------------------
if __name__ == "__main__":
    app.run(debug=Config.DEBUG)