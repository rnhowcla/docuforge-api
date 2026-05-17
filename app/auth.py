from functools import wraps
from flask import request, jsonify, g
from app.database import SessionLocal
from app.models import APIKey, Tier

LIMITS = {Tier.FREE: 50, Tier.PRO: 1000, Tier.BUSINESS: 5000}


def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get("X-API-Key")
        if not api_key:
            return jsonify({"detail": "Missing X-API-Key header"}), 422

        db = SessionLocal()
        key_hash = APIKey.hash_key(api_key)
        key = db.query(APIKey).filter(APIKey.key_hash == key_hash).first()
        if not key:
            db.close()
            return jsonify({"detail": "Invalid API key"}), 401

        limit = LIMITS.get(key.tier, 50)
        if key.call_count >= limit:
            db.close()
            return jsonify({"detail": "Rate limit exceeded. Upgrade your plan."}), 429

        g.api_key = key
        g.db = db
        return f(*args, **kwargs)

    return decorated
