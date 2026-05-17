"""Seed the database with an initial API key for testing."""
from app.database import engine, SessionLocal, Base
from app.models import APIKey, Tier

Base.metadata.create_all(bind=engine)


def seed():
    db = SessionLocal()
    existing = db.query(APIKey).first()
    if existing:
        print("Database already has keys. Skipping seed.")
        db.close()
        return

    raw, key_hash, prefix = APIKey.generate_key()
    key = APIKey(
        key_hash=key_hash,
        key_prefix=prefix,
        name="Test Key (Free)",
        tier=Tier.FREE,
    )
    db.add(key)

    # Create a Pro key for testing
    raw2, key_hash2, prefix2 = APIKey.generate_key()
    key2 = APIKey(
        key_hash=key_hash2,
        key_prefix=prefix2,
        name="Test Key (Pro)",
        tier=Tier.PRO,
    )
    db.add(key2)

    db.commit()
    print(f"Free tier key:  {raw}")
    print(f"Pro tier key:   {raw2}")
    print("\nUse these in the X-API-Key header.")
    db.close()


if __name__ == "__main__":
    seed()
