import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-in-production")
DOMAIN = os.getenv("DOMAIN", "http://localhost:8000")

# Rate limits (per API key)
FREE_TIER_LIMIT = 50
PRO_TIER_LIMIT = 1000
BUSINESS_TIER_LIMIT = 5000

# Admin
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
