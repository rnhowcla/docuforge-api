import io
from pypdf import PdfReader, PdfWriter


def extract_text(file_bytes: bytes, page_range: str | None = None) -> str:
    reader = PdfReader(io.BytesIO(file_bytes))
    pages = _parse_page_range(page_range, len(reader.pages)) if page_range else range(len(reader.pages))
    results = []
    for i in pages:
        page = reader.pages[i]
        text = page.extract_text()
        if text:
            results.append(f"--- Page {i+1} ---\n{text}")
    return "\n\n".join(results)


def extract_metadata(file_bytes: bytes) -> dict:
    reader = PdfReader(io.BytesIO(file_bytes))
    meta = reader.metadata
    return {
        "pages": len(reader.pages),
        "title": str(meta.title) if meta and meta.title else None,
        "author": str(meta.author) if meta and meta.author else None,
        "subject": str(meta.subject) if meta and meta.subject else None,
        "creator": str(meta.creator) if meta and meta.creator else None,
    }


def split_pdf(file_bytes: bytes, pages_per_split: int = 1) -> list[bytes]:
    reader = PdfReader(io.BytesIO(file_bytes))
    results = []
    total = len(reader.pages)
    for start in range(0, total, pages_per_split):
        writer = PdfWriter()
        end = min(start + pages_per_split, total)
        for i in range(start, end):
            writer.add_page(reader.pages[i])
        output = io.BytesIO()
        writer.write(output)
        output.seek(0)
        results.append(output.read())
    return results


def merge_pdfs(files: list[bytes]) -> bytes:
    writer = PdfWriter()
    for file_bytes in files:
        reader = PdfReader(io.BytesIO(file_bytes))
        for page in reader.pages:
            writer.add_page(page)
    output = io.BytesIO()
    writer.write(output)
    output.seek(0)
    return output.read()


def _parse_page_range(range_str: str, total: int) -> list[int]:
    pages = []
    for part in range_str.split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-")
            pages.extend(range(int(start) - 1, int(end)))
        else:
            pages.append(int(part) - 1)
    return [p for p in pages if 0 <= p < total]
