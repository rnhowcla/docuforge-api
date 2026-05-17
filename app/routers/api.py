from datetime import datetime, timezone
from flask import Blueprint, request, jsonify, g
from app.models import UsageLog
from app.auth import require_api_key
from app.services import excel_service, pdf_service, csv_service

api_bp = Blueprint("api", __name__, url_prefix="/api/v1")


def _log_usage(endpoint: str, status: str = "success"):
    g.db.add(UsageLog(api_key_id=g.api_key.id, endpoint=endpoint,
                      timestamp=datetime.now(timezone.utc), status=status))
    g.api_key.call_count += 1
    g.db.commit()


def _get_file(exts: tuple[str, ...]):
    f = None
    for key in request.files:
        f = request.files[key]
        break
    if not f or not f.filename:
        return None, (jsonify({"detail": "No file provided"}), 400)
    if not f.filename.lower().endswith(exts):
        return None, (jsonify({"detail": f"Only {exts} files are supported"}), 400)
    return f, None


@api_bp.route("/me", methods=["GET"])
@require_api_key
def me():
    return jsonify({
        "name": g.api_key.name,
        "tier": g.api_key.tier.value,
        "call_count": g.api_key.call_count,
        "created_at": g.api_key.created_at.isoformat(),
    })


@api_bp.route("/excel/clean", methods=["POST"])
@require_api_key
def excel_clean():
    f, err = _get_file((".xlsx", ".xls"))
    if err:
        return err
    try:
        remove_dup = request.form.get("remove_duplicates", "true") == "true"
        trim = request.form.get("trim_spaces", "true") == "true"
        result = excel_service.clean_excel(f.read(), remove_dup, trim)
        _log_usage("excel/clean")
        return jsonify({"filename": f"cleaned_{f.filename}", "size": len(result), "data": result.hex()})
    except Exception as e:
        _log_usage("excel/clean", "error")
        return jsonify({"detail": str(e)}), 500


@api_bp.route("/excel/to-csv", methods=["POST"])
@require_api_key
def excel_to_csv():
    f, err = _get_file((".xlsx", ".xls"))
    if err:
        return err
    try:
        sheet = request.form.get("sheet_name")
        result = excel_service.excel_to_csv(f.read(), sheet)
        _log_usage("excel/to-csv")
        return jsonify({"csv": result})
    except Exception as e:
        _log_usage("excel/to-csv", "error")
        return jsonify({"detail": str(e)}), 500


@api_bp.route("/excel/format", methods=["POST"])
@require_api_key
def excel_format():
    f, err = _get_file((".xlsx", ".xls"))
    if err:
        return err
    try:
        result = excel_service.format_excel(f.read())
        _log_usage("excel/format")
        return jsonify({"filename": f"formatted_{f.filename}", "size": len(result), "data": result.hex()})
    except Exception as e:
        _log_usage("excel/format", "error")
        return jsonify({"detail": str(e)}), 500


@api_bp.route("/csv/to-excel", methods=["POST"])
@require_api_key
def csv_to_excel():
    f, err = _get_file((".csv",))
    if err:
        return err
    try:
        delimiter = request.form.get("delimiter", ",")
        result = csv_service.csv_to_excel(f.read(), delimiter)
        _log_usage("csv/to-excel")
        name = f.filename.rsplit(".", 1)[0] + ".xlsx"
        return jsonify({"filename": name, "size": len(result), "data": result.hex()})
    except Exception as e:
        _log_usage("csv/to-excel", "error")
        return jsonify({"detail": str(e)}), 500


@api_bp.route("/csv/clean", methods=["POST"])
@require_api_key
def csv_clean():
    f, err = _get_file((".csv",))
    if err:
        return err
    try:
        delimiter = request.form.get("delimiter", ",")
        result = csv_service.csv_clean(f.read(), delimiter)
        _log_usage("csv/clean")
        return jsonify({"csv": result.decode("utf-8")})
    except Exception as e:
        _log_usage("csv/clean", "error")
        return jsonify({"detail": str(e)}), 500


@api_bp.route("/pdf/extract-text", methods=["POST"])
@require_api_key
def pdf_extract_text():
    f, err = _get_file((".pdf",))
    if err:
        return err
    try:
        page_range = request.form.get("page_range")
        result = pdf_service.extract_text(f.read(), page_range)
        _log_usage("pdf/extract-text")
        return jsonify({"text": result})
    except Exception as e:
        _log_usage("pdf/extract-text", "error")
        return jsonify({"detail": str(e)}), 500


@api_bp.route("/pdf/metadata", methods=["POST"])
@require_api_key
def pdf_metadata():
    f, err = _get_file((".pdf",))
    if err:
        return err
    try:
        result = pdf_service.extract_metadata(f.read())
        _log_usage("pdf/metadata")
        return jsonify(result)
    except Exception as e:
        _log_usage("pdf/metadata", "error")
        return jsonify({"detail": str(e)}), 500


@api_bp.route("/pdf/merge", methods=["POST"])
@require_api_key
def pdf_merge():
    files = request.files.getlist("files")
    if not files:
        return jsonify({"detail": "No files provided"}), 400
    try:
        file_bytes_list = [f.read() for f in files]
        result = pdf_service.merge_pdfs(file_bytes_list)
        _log_usage("pdf/merge")
        return jsonify({"filename": "merged.pdf", "size": len(result), "data": result.hex()})
    except Exception as e:
        _log_usage("pdf/merge", "error")
        return jsonify({"detail": str(e)}), 500
