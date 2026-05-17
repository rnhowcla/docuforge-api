import io
import pytest
from app.main import app
from app.database import Base, engine, SessionLocal
from app.models import APIKey, Tier

app.config["TESTING"] = True
client = app.test_client()


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def _make_key(tier=Tier.FREE) -> str:
    db = SessionLocal()
    raw, key_hash, _ = APIKey.generate_key()
    key = APIKey(key_hash=key_hash, key_prefix=raw[:12], name="T", tier=tier)
    db.add(key)
    db.commit()
    db.close()
    return raw


def test_landing_page():
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"DocuForge" in resp.data


def test_pricing_page():
    resp = client.get("/pricing")
    assert resp.status_code == 200
    assert b"Free" in resp.data


def test_api_without_key():
    resp = client.get("/api/v1/me")
    assert resp.status_code == 422


def test_api_with_bad_key():
    resp = client.get("/api/v1/me", headers={"X-API-Key": "bad-key"})
    assert resp.status_code == 401


def test_me_endpoint():
    raw = _make_key()
    resp = client.get("/api/v1/me", headers={"X-API-Key": raw})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["name"] == "T"
    assert data["tier"] == "free"


def test_excel_clean():
    raw = _make_key()
    import pandas as pd
    df = pd.DataFrame({"A": [1, 2, 2], "B": [" x ", " y ", " y "], "C": [3, 4, 4]})
    buf = io.BytesIO()
    df.to_excel(buf, index=False)
    buf.seek(0)
    resp = client.post(
        "/api/v1/excel/clean",
        data={"file": (buf, "test.xlsx"), "remove_duplicates": "true", "trim_spaces": "true"},
        headers={"X-API-Key": raw},
        content_type="multipart/form-data",
    )
    assert resp.status_code == 200
    assert "data" in resp.get_json()


def test_csv_to_excel():
    raw = _make_key()
    csv_content = b"name,age\nAlice,30\nBob,25"
    resp = client.post(
        "/api/v1/csv/to-excel",
        data={"file": (io.BytesIO(csv_content), "test.csv")},
        headers={"X-API-Key": raw},
        content_type="multipart/form-data",
    )
    assert resp.status_code == 200
    assert "data" in resp.get_json()


def test_pdf_extract_text():
    raw = _make_key()
    from pypdf import PdfWriter
    writer = PdfWriter()
    writer.add_blank_page(100, 100)
    buf = io.BytesIO()
    writer.write(buf)
    buf.seek(0)
    resp = client.post(
        "/api/v1/pdf/extract-text",
        data={"file": (buf, "test.pdf")},
        headers={"X-API-Key": raw},
        content_type="multipart/form-data",
    )
    assert resp.status_code == 200
    assert "text" in resp.get_json()
