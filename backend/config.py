import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DEBUG = os.getenv("FLASK_ENV", "development") == "development"
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwtsecretkey")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT expiration (seconds)
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv("JWT_ACCESS_EXPIRES", 900))      # 15 minutes
    JWT_REFRESH_TOKEN_EXPIRES = int(os.getenv("JWT_REFRESH_EXPIRES", 604800)) # 7 days

    # Rate limiter storage (Redis recommended)
    RATE_LIMITER_STORAGE = os.getenv("RATE_LIMITER_STORAGE", "redis://localhost:6379")

    # CORS origins - comma separated OR leave blank for allow all
    CORS_ORIGINS = [o.strip() for o in os.getenv("CORS_ORIGINS", "").split(",") if o.strip()]