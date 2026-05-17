from flask import Blueprint, render_template, request, redirect, url_for, session
from app.database import SessionLocal
from app.models import APIKey, UsageLog, Tier
from app.config import ADMIN_PASSWORD
from sqlalchemy import func

web_bp = Blueprint("web", __name__)


@web_bp.route("/")
def landing():
    return render_template("landing.html")


@web_bp.route("/pricing")
def pricing():
    return render_template("pricing.html")


@web_bp.route("/docs-page")
def docs_page():
    return render_template("docs.html")


@web_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    email = request.form.get("email", "").strip()
    name = request.form.get("name", "").strip() or email.split("@")[0]

    if not email or "@" not in email:
        return render_template("register.html", error="Please enter a valid email address.")

    db = SessionLocal()
    raw, key_hash, prefix = APIKey.generate_key()
    key = APIKey(key_hash=key_hash, key_prefix=prefix, name=name, email=email)
    db.add(key)
    db.commit()
    db.close()

    return render_template("key_ready.html", api_key=raw, name=name, prefix=prefix)


# ── Admin ──

@web_bp.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        pw = request.form.get("password", "")
        if pw == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect(url_for("web.admin_dashboard"))
        return render_template("admin_login.html", error="Wrong password")
    return render_template("admin_login.html")


@web_bp.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("admin"):
        return redirect(url_for("web.admin_login"))

    db = SessionLocal()
    total_users = db.query(APIKey).count()
    total_calls = db.query(func.sum(APIKey.call_count)).scalar() or 0
    free_count = db.query(APIKey).filter(APIKey.tier == Tier.FREE).count()
    pro_count = db.query(APIKey).filter(APIKey.tier == Tier.PRO).count()
    business_count = db.query(APIKey).filter(APIKey.tier == Tier.BUSINESS).count()

    # Recent users
    recent_users = db.query(APIKey).order_by(APIKey.created_at.desc()).limit(20).all()

    # Recent calls
    recent_logs = db.query(UsageLog).order_by(UsageLog.timestamp.desc()).limit(30).all()
    # Build endpoint -> count map for display
    endpoint_counts = {}
    for log in recent_logs:
        endpoint_counts[log.endpoint] = endpoint_counts.get(log.endpoint, 0) + 1

    db.close()

    return render_template(
        "admin_dashboard.html",
        total_users=total_users,
        total_calls=total_calls,
        free_count=free_count,
        pro_count=pro_count,
        business_count=business_count,
        recent_users=recent_users,
        recent_logs=recent_logs,
        endpoint_counts=endpoint_counts,
    )


@web_bp.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    return redirect(url_for("web.admin_login"))
