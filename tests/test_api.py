import io
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine, SessionLocal
from app.models import APIKey, Tier

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    raw, key_hash, prefix = APIKey.generate_key()
    key = APIKey(key_hash=key_hash, key_prefix=prefix, name="Test", tier=Tier.FREE)
    db.add(key)
    db.commit()
    db.close()
    yield
    Base.metadata.drop_all(bind=engine)


def test_landing_page():
    resp = client.get("/")
    assert resp.status_code == 200
    assert "DocuForge" in resp.text


def test_pricing_page():
    resp = client.get("/pricing")
    assert resp.status_code == 200
    assert "Free" in resp.text


def test_api_without_key():
    resp = client.get("/api/v1/me")
    assert resp.status_code == 422  # missing header


def test_api_with_bad_key():
    resp = client.get("/api/v1/me", headers={"X-API-Key": "bad-key"})
    assert resp.status_code == 401


def test_me_endpoint():
    db = SessionLocal()
    raw, key_hash, _ = APIKey.generate_key()
    key = APIKey(key_hash=key_hash, key_prefix=raw[:12], name="Test User", tier=Tier.FREE)
    db.add(key)
    db.commit()
    db.close()
    resp = client.get("/api/v1/me", headers={"X-API-Key": raw})
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == "Test User"
    assert data["tier"] == "free"


def test_excel_clean():
    db = SessionLocal()
    raw, key_hash, _ = APIKey.generate_key()
    key = APIKey(key_hash=key_hash, key_prefix=raw[:12], name="T", tier=Tier.FREE)
    db.add(key)
    db.commit()
    db.close()
    import pandas as pd
    df = pd.DataFrame({"A": [1, 2, 2], "B": [" x ", " y ", " y "], "C": [3, 4, 4]})
    buf = io.BytesIO()
    df.to_excel(buf, index=False)
    buf.seek(0)
    resp = client.post(
        "/api/v1/excel/clean",
        files={"file": ("test.xlsx", buf, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
        data={"remove_duplicates": "true", "trim_spaces": "true"},
        headers={"X-API-Key": raw},
    )
    assert resp.status_code == 200
    assert "data" in resp.json()


def test_csv_to_excel():
    db = SessionLocal()
    raw, key_hash, _ = APIKey.generate_key()
    key = APIKey(key_hash=key_hash, key_prefix=raw[:12], name="T", tier=Tier.FREE)
    db.add(key)
    db.commit()
    db.close()
    csv_content = b"name,age\nAlice,30\nBob,25"
    resp = client.post(
        "/api/v1/csv/to-excel",
        files={"file": ("test.csv", csv_content, "text/csv")},
        headers={"X-API-Key": raw},
    )
    assert resp.status_code == 200
    assert "data" in resp.json()


def test_pdf_extract_text():
    db = SessionLocal()
    raw, key_hash, _ = APIKey.generate_key()
    key = APIKey(key_hash=key_hash, key_prefix=raw[:12], name="T", tier=Tier.FREE)
    db.add(key)
    db.commit()
    db.close()
    from pypdf import PdfWriter
    writer = PdfWriter()
    writer.add_blank_page(100, 100)
    buf = io.BytesIO()
    writer.write(buf)
    buf.seek(0)
    resp = client.post(
        "/api/v1/pdf/extract-text",
        files={"file": ("test.pdf", buf, "application/pdf")},
        headers={"X-API-Key": raw},
    )
    assert resp.status_code == 200
    assert "text" in resp.json()
