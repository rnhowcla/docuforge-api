from flask import Flask, g
from app.database import engine, Base, SessionLocal
from app.routers.api import api_bp
from app.routers.dashboard import web_bp
from app.config import SECRET_KEY

Base.metadata.create_all(bind=engine)

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024  # 50MB max upload

app.register_blueprint(api_bp)
app.register_blueprint(web_bp)


@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()
