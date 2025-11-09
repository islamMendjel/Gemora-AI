import logging
from logging.handlers import RotatingFileHandler
import os

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

log_path = os.path.join(LOG_DIR, "app.log")
err_log_path = os.path.join(LOG_DIR, "errors.log")

logger = logging.getLogger("chatbot")
logger.setLevel(logging.DEBUG)  # root logger level

# File handler for INFO+ (general)
file_handler = RotatingFileHandler(log_path, maxBytes=5*1024*1024, backupCount=5)
file_handler.setLevel(logging.INFO)
file_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

# File handler for ERROR only
error_handler = RotatingFileHandler(err_log_path, maxBytes=5*1024*1024, backupCount=5)
error_handler.setLevel(logging.ERROR)
error_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
error_handler.setFormatter(error_formatter)
logger.addHandler(error_handler)

# Console handler for debug (dev)
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
console_formatter = logging.Formatter("[%(levelname)s] %(message)s")
console.setFormatter(console_formatter)
logger.addHandler(console)
