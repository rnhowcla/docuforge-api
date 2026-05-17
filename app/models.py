import secrets
import hashlib
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, Enum as SAEnum
from app.database import Base
import enum


class Tier(str, enum.Enum):
    FREE = "free"
    PRO = "pro"
    BUSINESS = "business"


class APIKey(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, autoincrement=True)
    key_hash = Column(String, unique=True, nullable=False)
    key_prefix = Column(String, nullable=False)  # First 8 chars for display
    name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    tier = Column(SAEnum(Tier), default=Tier.FREE, nullable=False)
    call_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    @staticmethod
    def generate_key() -> tuple[str, str, str]:
        raw = "docu_" + secrets.token_hex(24)
        key_hash = hashlib.sha256(raw.encode()).hexdigest()
        return raw, key_hash, raw[:12]

    @staticmethod
    def hash_key(key: str) -> str:
        return hashlib.sha256(key.encode()).hexdigest()


class UsageLog(Base):
    __tablename__ = "usage_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    api_key_id = Column(Integer, nullable=False)
    endpoint = Column(String, nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    status = Column(String, default="success")
