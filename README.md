# DocuForge API

Document processing API for developers. Clean Excel, convert CSV, extract PDF text — all through simple REST endpoints.

## Quick Start

1. Register at **http://[2409:893d:dcd:8c60:3058:eb94:1d9:c7fa]:5000/register** to get your free API key.
2. **50 calls/month free** — no credit card required.

```bash
curl -X POST http://[2409:893d:dcd:8c60:3058:eb94:1d9:c7fa]:5000/api/v1/excel/clean \
  -H "X-API-Key: YOUR_KEY" \
  -F "file=@data.xlsx"
```

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/v1/excel/clean | Deduplicate, trim, clean Excel |
| POST | /api/v1/excel/to-csv | Convert Excel to CSV |
| POST | /api/v1/excel/format | Auto-fit columns, style headers |
| POST | /api/v1/csv/to-excel | Convert CSV to Excel |
| POST | /api/v1/csv/clean | Trim cells, remove empty rows |
| POST | /api/v1/pdf/extract-text | Extract text from PDF |
| POST | /api/v1/pdf/metadata | Get PDF info (pages, author, etc.) |
| POST | /api/v1/pdf/merge | Merge multiple PDFs |
| GET | /api/v1/me | View your API key info |

## Pricing

| Tier | Calls/Month | Price |
|------|-------------|-------|
| Free | 50 | $0 |
| Pro | 1,000 | $9/mo |
| Business | 5,000 | $29/mo |

Visit [the pricing page](http://[2409:893d:dcd:8c60:3058:eb94:1d9:c7fa]:5000/pricing) to upgrade.

## Self-Host

```bash
git clone https://github.com/rnhowcla/docuforge-api.git
cd docuforge-api
pip install -r requirements.txt
python seed.py
flask --app app.main run
```

## Tech Stack

Python Flask + SQLAlchemy + SQLite

## License

MIT
