import os, json, hashlib, time
from collections import OrderedDict

# Fallback-safe Redis import
try:
    from redis import Redis
    REDIS_AVAILABLE = True
except ImportError:
    Redis = None
    REDIS_AVAILABLE = False

REDIS_URL = os.getenv("RATE_LIMITER_STORAGE", "memory://")

# Fallback in-memory cache
_memory_cache = OrderedDict()
_MAX_MEM_CACHE = 200  # entries

def _make_key(user_id: str, prompt: str):
    h = hashlib.sha256()
    h.update(prompt.encode("utf-8"))
    return f"gemini:{user_id}:{h.hexdigest()}"

def get_cached_response(user_id: str, prompt: str):
    key = _make_key(user_id, prompt)
    if REDIS_AVAILABLE and REDIS_URL.startswith("redis://"):
        try:
            r = Redis.from_url(REDIS_URL, decode_responses=True)
            raw = r.get(key)
            if raw:
                return json.loads(raw).get("response")
        except Exception:
            pass
    else:
        entry = _memory_cache.get(key)
        if entry and (time.time() - entry["ts"] < 3600):
            return entry["response"]
    return None

def set_cached_response(user_id: str, prompt: str, response: str, ttl: int = 3600):
    key = _make_key(user_id, prompt)
    payload = {"response": response, "ts": time.time()}
    if REDIS_AVAILABLE and REDIS_URL.startswith("redis://"):
        try:
            r = Redis.from_url(REDIS_URL, decode_responses=True)
            r.setex(key, ttl, json.dumps(payload))
            return
        except Exception:
            pass
    _memory_cache[key] = payload
    if len(_memory_cache) > _MAX_MEM_CACHE:
        _memory_cache.popitem(last=False)
