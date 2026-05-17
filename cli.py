"""CLI for managing API keys. Usage: python cli.py <command>"""
import sys
from app.database import engine, SessionLocal, Base
from app.models import APIKey, Tier

Base.metadata.create_all(bind=engine)


def create_key(name: str, tier: str = "free"):
    db = SessionLocal()
    t = Tier(tier) if tier in [t.value for t in Tier] else Tier.FREE
    raw, key_hash, prefix = APIKey.generate_key()
    key = APIKey(key_hash=key_hash, key_prefix=prefix, name=name, tier=t)
    db.add(key)
    db.commit()
    print(f"Created key: {raw}")
    print(f"  Name: {name} | Tier: {t.value} | Prefix: {prefix}")
    db.close()


def list_keys():
    db = SessionLocal()
    keys = db.query(APIKey).all()
    if not keys:
        print("No API keys found.")
    for k in keys:
        print(f"  [{k.tier.value.upper():8}] {k.key_prefix}... | {k.name} | {k.call_count} calls | {k.created_at.strftime('%Y-%m-%d')}")
    db.close()


def revoke_key(prefix: str):
    db = SessionLocal()
    key = db.query(APIKey).filter(APIKey.key_prefix.startswith(prefix)).first()
    if not key:
        print(f"No key found with prefix '{prefix}'")
    else:
        db.delete(key)
        db.commit()
        print(f"Revoked key: {key.key_prefix}... ({key.name})")
    db.close()


def reset_usage():
    db = SessionLocal()
    count = db.query(APIKey).count()
    db.query(APIKey).update({"call_count": 0})
    db.commit()
    print(f"Reset usage for {count} keys.")
    db.close()


if __name__ == "__main__":
    cmds = {"create": create_key, "list": list_keys, "revoke": revoke_key, "reset": reset_usage}
    if len(sys.argv) < 2 or sys.argv[1] not in cmds:
        print("Usage: python cli.py <create|list|revoke|reset> [args]")
        print("  create <name> [free|pro|business]")
        print("  list")
        print("  revoke <key_prefix>")
        print("  reset  (reset all usage counters)")
        sys.exit(1)

    cmd = sys.argv[1]
    args = sys.argv[2:]
    if cmd == "create":
        if not args:
            print("Usage: python cli.py create <name> [tier]")
            sys.exit(1)
        create_key(*args)
    elif cmd == "revoke":
        if not args:
            print("Usage: python cli.py revoke <key_prefix>")
            sys.exit(1)
        revoke_key(args[0])
    elif cmd == "list":
        list_keys()
    elif cmd == "reset":
        reset_usage()
