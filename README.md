# MCP Universal EC E-Invoice Server

An [MCP (Model Context Protocol)](https://modelcontextprotocol.io/) server wrapping the **Universal EC (汎宇電商) Taiwan E-Invoice POS Web Service** (JSON format, MIG4.1). Exposes 27 AI-callable tools covering all available function codes via stdio JSON-RPC 2.0.

Part of the [Asgard AI Platform](https://github.com/asgard-ai-platform) open-source ecosystem.

[繁體中文](README.zh-TW.md)

## Features

- **27 MCP tools** — Full coverage of all Universal EC e-invoice API function codes
- **stdio JSON-RPC 2.0** — Standard MCP transport protocol
- **3 wrapper formats** — INDEX, Invoice, Allowance (auto-selected per function)
- **Credential injection** — SELLERID/POSID/POSSN auto-injected by connector
- **TDD tested** — 53 unit tests + 5 live regression tests

## Quick Start

```bash
# Setup
uv venv && source .venv/bin/activate
uv pip install -e ".[dev]"

# Configure credentials
cp .env.example .env
# Edit .env with your Universal EC credentials

# Run server
python mcp_server.py
```

## Configuration

Create a `.env` file with your Universal EC POS credentials:

```
EINVOICE_BASE_URL=https://epostw.einvoice.com.tw/GetInvoice.ashx
EINVOICE_SELLER_ID=your_seller_id
EINVOICE_POS_ID=your_pos_id
EINVOICE_POS_SN=your_pos_sn
```

| Environment | URL |
|---|---|
| Test (測試機) | `https://epostw.einvoice.com.tw/GetInvoice.ashx` |
| Production (正式機) | `https://eposw.einvoice.com.tw/GetInvoice.ashx` |

## Project Structure

```
mcp-universalec-e-invoice/
├── app.py                          # FastMCP singleton
├── mcp_server.py                   # Entry point (stdio transport)
├── config/
│   └── settings.py                 # URL + credentials from .env
├── connectors/
│   └── einvoice_client.py          # Single POST connector (3 wrappers)
├── tools/
│   ├── system_tools.py             # Y01
│   ├── invoice_number_tools.py     # A01, C01, Z21, Z22
│   ├── b2c_invoice_tools.py        # C0401, C0401N, C0501
│   ├── b2b_invoice_tools.py        # A0401, A0501, A0101, A0201
│   ├── allowance_tools.py          # D0401, D0401N, D0501, B0401, B0501, B0101
│   ├── cancel_tools.py             # C0701, B0701
│   ├── query_tools.py              # Z11, Z31, Z33, Z34
│   └── admin_tools.py              # Z32, E0401, E0402
└── tests/
    ├── conftest.py                 # Shared fixtures
    ├── test_einvoice_client.py     # Connector unit tests
    ├── test_system_tools.py        # Y01 tests
    ├── test_invoice_number_tools.py
    ├── test_b2c_invoice_tools.py
    ├── test_b2b_invoice_tools.py
    ├── test_allowance_tools.py
    ├── test_cancel_tools.py
    ├── test_query_tools.py
    ├── test_admin_tools.py
    └── test_regression.py          # Live API tests
```

## Tools (27 total)

### System
| Tool | Code | Description |
|---|---|---|
| `get_system_time` | Y01 | Connection test / get server time |

### Invoice Number Management
| Tool | Code | Description |
|---|---|---|
| `get_invoice_numbers` | A01 | Get invoice number allocation (current period) |
| `get_next_period_numbers` | C01 | Get invoice number allocation (next period) |
| `get_invoice_numbers_expanded` | Z21 | Get numbers expanded per-invoice with AESKEY |
| `get_next_period_numbers_expanded` | Z22 | Get next period numbers expanded with AESKEY |

### B2C Invoices
| Tool | Code | Description |
|---|---|---|
| `create_b2c_invoice` | C0401 | Create B2C invoice (positional field format) |
| `create_b2c_invoice_named` | C0401N | Create B2C invoice (named field format) |
| `void_b2c_invoice` | C0501 | Void a B2C invoice |

### B2B Invoices
| Tool | Code | Description |
|---|---|---|
| `create_b2b_invoice` | A0401 | Create B2B invoice (platform certified) |
| `void_b2b_invoice` | A0501 | Void a B2B invoice |
| `create_b2b_exchange_invoice` | A0101 | Create B2B exchange invoice |
| `void_b2b_exchange_invoice` | A0201 | Void a B2B exchange invoice |

### Allowances (折讓)
| Tool | Code | Description |
|---|---|---|
| `create_b2c_allowance` | D0401 | Create B2C allowance |
| `create_b2c_allowance_named` | D0401N | Create B2C allowance (named format) |
| `void_b2c_allowance` | D0501 | Void a B2C allowance |
| `create_b2b_allowance` | B0401 | Create B2B allowance |
| `void_b2b_allowance` | B0501 | Void a B2B allowance |
| `create_b2b_exchange_allowance` | B0101 | Create B2B exchange allowance |

### Cancellation (註銷)
| Tool | Code | Description |
|---|---|---|
| `cancel_invoice` | C0701 | Cancel an invoice |
| `batch_cancel_invoice` | B0701 | Batch cancel with full invoice data |

### Queries
| Tool | Code | Description |
|---|---|---|
| `get_cancel_status` | Z11 | Get invoice cancel process status |
| `get_downloaded_track_ranges` | Z31 | Query downloaded track ranges |
| `get_assignment_info` | Z33 | Query tax ID number assignment |
| `get_winning_list` | Z34 | Download winning invoice list |

### Administration
| Tool | Code | Description |
|---|---|---|
| `upload_next_period_tracks` | Z32 | Upload next period track numbers |
| `assign_branch_tracks` | E0401 | Branch office track assignment |
| `report_unused_tracks` | E0402 | Report unused track ranges |

## Usage Examples

Once the MCP server is running, an AI assistant (e.g. Claude) can call these tools on your behalf. Here are real-world scenarios showing what you say and how the AI responds.

---

### "Help me check if the e-invoice system is connected"

> **You:** 幫我測試一下電子發票系統有沒有連線成功

**AI calls:** `get_system_time()`

**Result:** The system returns `REPLY: "1"` with `MESSAGE: "連線成功"` and the server time `2026/04/01 22:29:03`. Your connection is working.

---

### "What invoice numbers do I have available right now?"

> **You:** 我目前有哪些可用的發票號碼？

**AI calls:** `get_invoice_numbers()`

**Result:** Current period is 115 年 03-04 月, track `GS`, numbers `82775400` ~ `82775449` (50 invoices available). The AI can also explain the QRCode AES key returned for barcode generation.

---

### "I need to get the detailed invoice numbers with AES keys for printing"

> **You:** 我需要取得每張發票的 AESKEY 跟隨機碼，準備列印用

**AI calls:** `get_invoice_numbers_expanded()`

**Result:** Returns 50 individual invoices, each with its own number, AESKEY, and random number:
```
GS82775450 → AESKEY: Xymp9aqy..., RandomNumber: 7833
GS82775451 → AESKEY: XausdWBO..., RandomNumber: 4581
...
```

---

### "Issue an invoice for a customer who bought 2 lattes and 1 cake"

> **You:** 幫我開一張發票，客人買了 2 杯拿鐵 65 元、1 個巧克力蛋糕 85 元，總共 215 元含稅，紙本發票已列印

**AI calls:** `get_invoice_numbers_expanded()` to get an available number, then:

```
create_b2c_invoice(
  invoice_number = "GS82775402",     ← from the allocation
  invoice_date   = "2026-04-01",
  invoice_time   = "14:30:00",
  buyer_id       = "0000000000",     ← consumer, no tax ID
  buyer_name     = "0000",
  invoice_type   = "07",
  donate_mark    = "0",
  print_mark     = "Y",
  random_number  = "6136",           ← from the allocation
  tax_type = "1", tax_rate = "0.05", tax_amount = "10",
  sales_amount = "205", free_tax = "0", zero_tax = "0", total = "215",
  items = [
    {B1:"1", B2:"拿鐵咖啡", B3:"2", B5:"65", B6:"130", B7:"1", B13:"1"},
    {B1:"2", B2:"巧克力蛋糕", B3:"1", B5:"85", B6:"85", B7:"2", B13:"1"},
  ]
)
```

**Result:** `REPLY: "1"`, `MESSAGE: "成功"`, invoice `GS82775402` created.

---

### "Please void invoice GS82775401"

> **You:** 請幫我作廢發票 GS82775401，原因是客戶取消訂單

**AI calls:**
```
void_b2c_invoice(
  invoice_number = "GS82775401",
  invoice_date   = "2026-04-01",
  buyer_id       = "0000000000",
  seller_id      = "23997652",
  cancel_date    = "2026-04-01",
  cancel_time    = "15:00:00",
  cancel_reason  = "客戶取消訂單",
)
```

**Result:** `REPLY: "1"`, `MESSAGE: "成功"` — invoice voided successfully.

---

### "Check the cancellation status of invoice GS82775400"

> **You:** 幫我查一下 GS82775400 這張發票的註銷狀態

**AI calls:** `get_cancel_status(invoice_number="GS82775400", invoice_date="2026-04-01")`

**Result:** `STATUSCODE: "1"` = completed, `"2"` = pending, `"3"` = failed. The AI interprets and tells you the current status in plain language.

---

### "Cancel invoice GS82775400 — it was issued by mistake"

> **You:** 發票 GS82775400 開錯了，幫我註銷

**AI calls:**
```
cancel_invoice(
  invoice_number = "GS82775400",
  invoice_date   = "2026-04-01",
  buyer_id       = "0000000000",
  seller_id      = "23997652",
  cancel_date    = "2026-04-01",
  cancel_time    = "16:00:00",
  cancel_reason  = "誤開發票",
)
```

**Result:** If the invoice has been uploaded to the tax authority, `REPLY: "1"` confirms cancellation. If it hasn't been uploaded yet, the system returns `REPLY: "-1"` with a message explaining the invoice is still being processed — the AI will tell you to try again later.

> **Note:** "作廢" (C0501 void) and "註銷" (C0701 cancel) are different. Void happens before upload to tax authority; cancel happens after. The AI picks the right tool based on context.

---

### "I need to check what invoice number ranges have been downloaded"

> **You:** 查一下統編 23997652 在 11504 期的 GS 字軌已下載的配號區間

**AI calls:**
```
get_downloaded_track_ranges(
  head_ban      = "23997652",
  branch_ban    = "23997652",
  invoice_type  = "07",
  year_month    = "11504",
  invoice_track = "GS",
)
```

**Result:** Returns the track ranges that have been successfully downloaded for this period.

## Testing

```bash
# Unit tests (mocked HTTP, no credentials needed)
pytest tests/ --ignore=tests/test_regression.py -v

# Regression tests (requires .env with valid credentials)
pytest tests/test_regression.py -v -s
```

## Architecture

All 27 functions communicate through a single POST endpoint (`GetInvoice.ashx`), differentiated by function code in the JSON body. The connector auto-injects credentials (SELLERID, POSID, POSSN) and system time.

Three JSON wrapper formats:
- **INDEX** — System/number functions (Y01, A01, C01, Z21, Z22, Z11)
- **Invoice** — Invoice/allowance/admin CRUD (C0401, A0401, D0401, C0701, E0401, Z31, etc.)
- **Allowance** — B0501 only (void B2B allowance)

## License

MIT License — see [LICENSE](LICENSE) for details.

## Part of the Asgard Ecosystem

See the full [Asgard AI Platform](https://github.com/asgard-ai-platform) for more MCP servers.
