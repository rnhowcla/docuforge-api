# DocuForge API — Document Processing Made Simple

Transform Excel, CSV, and PDF files through a clean REST API. No heavy libraries, no Excel installation needed.

## Quick Start

Register at [http://[2409:893d:dcd:8c60:3058:eb94:1d9:c7fa]:5000/register](http://[2409:893d:dcd:8c60:3058:eb94:1d9:c7fa]:5000/register) — **50 calls/month free, no credit card required.**



## All Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/v1/excel/clean | Deduplicate rows, trim whitespace, clean data |
| POST | /api/v1/excel/to-csv | Convert Excel (.xlsx/.xls) to CSV |
| POST | /api/v1/excel/format | Auto-fit columns, bold headers, borders |
| POST | /api/v1/csv/to-excel | Convert CSV back to formatted Excel |
| POST | /api/v1/csv/clean | Trim cells, remove empty rows, normalize encoding |
| POST | /api/v1/pdf/extract-text | Extract text content from PDF files |
| POST | /api/v1/pdf/metadata | Get page count, author, title, creation date |
| POST | /api/v1/pdf/merge | Combine multiple PDFs into one |
| GET | /api/v1/me | View your API key status and usage |

## Pricing

| Tier | Calls/Month | Price |
|------|-------------|-------|
| **Free** | 50 | /usr/bin/bash |
| **Pro** | 1,000 | /mo |
| **Business** | 5,000 | 9/mo |

[Upgrade in the dashboard](http://[2409:893d:dcd:8c60:3058:eb94:1d9:c7fa]:5000/pricing)

## Python Example



## Tech Stack

Python • Flask • SQLAlchemy • SQLite • OpenPyXL • PyPDF2

## Self-Host



## License

MIT — use it, fork it, ship it.

---

Built by [@rnhowcla](https://github.com/rnhowcla) • [Live Demo](http://[2409:893d:dcd:8c60:3058:eb94:1d9:c7fa]:5000)
