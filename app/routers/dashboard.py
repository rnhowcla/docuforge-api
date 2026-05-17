from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.database import SessionLocal
from app.models import APIKey

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
