from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import Config

uri = Config.RATE_LIMITER_STORAGE or "memory://"
if uri.startswith("redis://"):
    storage_uri = uri
else:
    storage_uri = "memory://"

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per hour"],
    storage_uri=storage_uri
)
