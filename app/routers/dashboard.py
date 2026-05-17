from flask import Blueprint, render_template

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
