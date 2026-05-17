# 推广文案

## V2EX 帖子 (/go/create)

**标题：** 我做了个文档处理 API，Excel/CSV/PDF 自动化处理，送 50 次免费调用

**正文：**

自己做了一个文档处理 API 服务（DocuForge），可以：

- Excel 去重空格 / 转 CSV / 自动格式化
- CSV 转 Excel / 数据清洗
- PDF 提取文本和元数据 / 多文件合并

每个接口一个 POST 请求就搞定，注册即送 50 次/月免费额度。

技术栈：Python Flask + SQLAlchemy，代码已经在 GitHub 开源。

免费注册拿 Key：http://[2409:893d:dcd:8c60:3058:eb94:1d9:c7fa]:5000/register
GitHub：[https://github.com/rnhowcla/docuforge-api](https://github.com/rnhowcla/docuforge-api)

求各位开发者大佬试用给反馈，提意见直接 issue 或者回复里说。

---

## 掘金文章

**标题：** 手搓一个文档处理 API，从 0 到上线全过程

**大纲：**
1. 为什么做这个 — 工作中经常要做 Excel/CSV/PDF 的脏活
2. 技术选型 — Flask + SQLAlchemy + serveo 免费部署
3. API 设计 — RESTful，API Key 鉴权，三级限频
4. 核心代码 — Excel 清洗、CSV 互转、PDF 提取的实现
5. 部署上线 — 免费方案全记录
6. 商业模式 — freemium，注册送 50 次

---

## 知乎回答模板

搜索问题：「如何用 Python 批量处理 Excel 文件？」
回答：贴代码示例 + 顺便提自己的 API
```

---

## Readme 优化后的文案

```
# DocuForge API

Document processing API for developers. Clean Excel, convert CSV, extract PDF text — all through simple REST endpoints.

## Quick Start

Register at http://[2409:893d:dcd:8c60:3058:eb94:1d9:c7fa]:5000/register to get your free API key. 50 calls/month free.

curl -X POST http://[2409:893d:dcd:8c60:3058:eb94:1d9:c7fa]:5000/api/v1/excel/clean \
  -H "X-API-Key: YOUR_KEY" \
  -F "file=@data.xlsx"

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/v1/excel/clean | Deduplicate, trim, clean Excel |
| POST | /api/v1/excel/to-csv | Convert Excel to CSV |
| POST | /api/v1/excel/format | Auto-fit columns, style headers |
| POST | /api/v1/csv/to-excel | Convert CSV to Excel |
| POST | /api/v1/csv/clean | Trim cells, remove empty rows |
| POST | /api/v1/pdf/extract-text | Extract text from PDF |
| POST | /api/v1/pdf/metadata | Get PDF info (pages, author...) |
| POST | /api/v1/pdf/merge | Merge multiple PDFs |
| GET | /api/v1/me | View your API key info |

## Pricing

- **Free** — 50 calls/month
- **Pro** — 1,000 calls/month, $9
- **Business** — 5,000 calls/month, $29

## Self-Host

git clone https://github.com/rnhowcla/docuforge-api.git
cd docuforge-api
pip install -r requirements.txt
python seed.py
flask --app app.main run
```
