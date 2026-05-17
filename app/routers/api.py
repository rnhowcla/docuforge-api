from datetime import datetime, timezone
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import APIKey, UsageLog
from app.auth import get_api_key
from app.services import excel_service, pdf_service, csv_service

router = APIRouter(prefix="/api/v1", tags=["API"])


def _log_usage(db: Session, key: APIKey, endpoint: str, status: str = "success"):
    db.add(UsageLog(api_key_id=key.id, endpoint=endpoint, timestamp=datetime.now(timezone.utc), status=status))
    key.call_count += 1
    db.commit()


@router.get("/me")
def api_key_info(key: APIKey = Depends(get_api_key)):
    return {
        "name": key.name,
        "tier": key.tier.value,
        "call_count": key.call_count,
        "created_at": key.created_at.isoformat(),
    }


@router.post("/excel/clean")
def excel_clean(
    file: UploadFile = File(...),
    remove_duplicates: bool = Form(True),
    trim_spaces: bool = Form(True),
    key: APIKey = Depends(get_api_key),
    db: Session = Depends(get_db),
):
    if not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(400, "Only .xlsx and .xls files are supported")
    try:
        result = excel_service.clean_excel(file.file.read(), remove_duplicates, trim_spaces)
        _log_usage(db, key, "excel/clean")
        return {"filename": f"cleaned_{file.filename}", "size": len(result), "data": result.hex()}
    except Exception as e:
        _log_usage(db, key, "excel/clean", "error")
        raise HTTPException(500, str(e))


@router.post("/excel/to-csv")
def excel_to_csv(
    file: UploadFile = File(...),
    sheet_name: str | None = Form(None),
    key: APIKey = Depends(get_api_key),
    db: Session = Depends(get_db),
):
    if not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(400, "Only .xlsx and .xls files are supported")
    try:
        result = excel_service.excel_to_csv(file.file.read(), sheet_name)
        _log_usage(db, key, "excel/to-csv")
        return {"csv": result}
    except Exception as e:
        _log_usage(db, key, "excel/to-csv", "error")
        raise HTTPException(500, str(e))


@router.post("/excel/format")
def excel_format(
    file: UploadFile = File(...),
    key: APIKey = Depends(get_api_key),
    db: Session = Depends(get_db),
):
    if not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(400, "Only .xlsx and .xls files are supported")
    try:
        result = excel_service.format_excel(file.file.read())
        _log_usage(db, key, "excel/format")
        return {"filename": f"formatted_{file.filename}", "size": len(result), "data": result.hex()}
    except Exception as e:
        _log_usage(db, key, "excel/format", "error")
        raise HTTPException(500, str(e))


@router.post("/csv/to-excel")
def csv_to_excel(
    file: UploadFile = File(...),
    delimiter: str = Form(","),
    key: APIKey = Depends(get_api_key),
    db: Session = Depends(get_db),
):
    if not file.filename.endswith(".csv"):
        raise HTTPException(400, "Only .csv files are supported")
    try:
        result = csv_service.csv_to_excel(file.file.read(), delimiter)
        _log_usage(db, key, "csv/to-excel")
        return {"filename": f"{file.filename.rsplit('.', 1)[0]}.xlsx", "size": len(result), "data": result.hex()}
    except Exception as e:
        _log_usage(db, key, "csv/to-excel", "error")
        raise HTTPException(500, str(e))


@router.post("/csv/clean")
def csv_clean(
    file: UploadFile = File(...),
    delimiter: str = Form(","),
    key: APIKey = Depends(get_api_key),
    db: Session = Depends(get_db),
):
    if not file.filename.endswith(".csv"):
        raise HTTPException(400, "Only .csv files are supported")
    try:
        result = csv_service.csv_clean(file.file.read(), delimiter)
        _log_usage(db, key, "csv/clean")
        return {"csv": result.decode("utf-8")}
    except Exception as e:
        _log_usage(db, key, "csv/clean", "error")
        raise HTTPException(500, str(e))


@router.post("/pdf/extract-text")
def pdf_extract_text(
    file: UploadFile = File(...),
    page_range: str | None = Form(None),
    key: APIKey = Depends(get_api_key),
    db: Session = Depends(get_db),
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(400, "Only .pdf files are supported")
    try:
        result = pdf_service.extract_text(file.file.read(), page_range)
        _log_usage(db, key, "pdf/extract-text")
        return {"text": result}
    except Exception as e:
        _log_usage(db, key, "pdf/extract-text", "error")
        raise HTTPException(500, str(e))


@router.post("/pdf/metadata")
def pdf_metadata(
    file: UploadFile = File(...),
    key: APIKey = Depends(get_api_key),
    db: Session = Depends(get_db),
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(400, "Only .pdf files are supported")
    try:
        result = pdf_service.extract_metadata(file.file.read())
        _log_usage(db, key, "pdf/metadata")
        return result
    except Exception as e:
        _log_usage(db, key, "pdf/metadata", "error")
        raise HTTPException(500, str(e))


@router.post("/pdf/merge")
def pdf_merge(
    files: list[UploadFile] = File(...),
    key: APIKey = Depends(get_api_key),
    db: Session = Depends(get_db),
):
    try:
        file_bytes_list = [f.file.read() for f in files]
        result = pdf_service.merge_pdfs(file_bytes_list)
        _log_usage(db, key, "pdf/merge")
        return {"filename": "merged.pdf", "size": len(result), "data": result.hex()}
    except Exception as e:
        _log_usage(db, key, "pdf/merge", "error")
        raise HTTPException(500, str(e))
