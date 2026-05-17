from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import APIKey, Tier
from app.config import FREE_TIER_LIMIT, PRO_TIER_LIMIT, BUSINESS_TIER_LIMIT

LIMITS = {Tier.FREE: FREE_TIER_LIMIT, Tier.PRO: PRO_TIER_LIMIT, Tier.BUSINESS: BUSINESS_TIER_LIMIT}


def get_api_key(x_api_key: str = Header(..., alias="X-API-Key"), db: Session = Depends(get_db)) -> APIKey:
    key_hash = APIKey.hash_key(x_api_key)
    key = db.query(APIKey).filter(APIKey.key_hash == key_hash).first()
    if not key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    limit = LIMITS.get(key.tier, FREE_TIER_LIMIT)
    if key.call_count >= limit:
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Upgrade your plan.")
    return key
