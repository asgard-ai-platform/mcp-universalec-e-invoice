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

Below are real examples tested against the Universal EC test environment.

### Example 1: Connection Test (Y01)

```python
from tools.system_tools import get_system_time

result = get_system_time()
# Response:
# {
#   "INDEX": {
#     "FUNCTIONCODE": "Y01",
#     "REPLY": "1",
#     "MESSAGE": "連線成功",
#     "SYSTIME": "2026/04/01 22:29:03",
#     ...
#   }
# }
```

### Example 2: Get Invoice Numbers (A01)

```python
from tools.invoice_number_tools import get_invoice_numbers

result = get_invoice_numbers()
# Response:
# {
#   "INDEX": {
#     "FUNCTIONCODE": "A01",
#     "REPLY": "1",
#     "MESSAGE": "成功",
#     "TAXMONTH": "11504",          ← invoice period (民國 115 年 03-04 月)
#     "INVOICEHEADER": "GS",        ← 2-letter track
#     "INVOICESTART": "82775400",   ← start number
#     "INVOICEEND": "82775449",     ← end number (50 invoices)
#     "QRCodeASKey": "D016F2FF...", ← AES key for QR code
#     "TYPE": "07"                  ← invoice type
#   }
# }
```

### Example 3: Get Expanded Numbers with AESKEY (Z21)

Each invoice gets its own AESKEY and random number for QR code generation.

```python
from tools.invoice_number_tools import get_invoice_numbers_expanded

result = get_invoice_numbers_expanded()
# Response includes INVOICEDATA array with per-invoice details:
# {
#   "INDEX": {
#     "FUNCTIONCODE": "Z21",
#     "REPLY": "1",
#     "INVOICEDATA": [
#       {
#         "INVOICE_NUMBER": "GS82775450",
#         "AESKEY": "Xymp9aqynK4N2jSIYLj1Lg==",
#         "RANDOMNUMBER": "7833",
#         "TAXMONTH": "11504"
#       },
#       {
#         "INVOICE_NUMBER": "GS82775451",
#         "AESKEY": "XausdWBOIH+SYm6DOSgInQ==",
#         "RANDOMNUMBER": "4581",
#         "TAXMONTH": "11504"
#       },
#       ...  ← up to 50 invoices per allocation
#     ]
#   }
# }
```

### Example 4: Create B2C Invoice (C0401)

```python
from tools.b2c_invoice_tools import create_b2c_invoice

result = create_b2c_invoice(
    invoice_number="GS82775401",
    invoice_date="2026-04-01",
    invoice_time="22:35:00",
    buyer_id="0000000000",       # consumer (no tax ID)
    buyer_name="0000",           # auto-converts to 4 random digits
    invoice_type="07",
    donate_mark="0",             # not a donation
    print_mark="Y",              # paper invoice printed
    random_number="5678",
    tax_type="1",                # taxable
    tax_rate="0.05",
    tax_amount="5",
    sales_amount="95",
    free_tax="0",
    zero_tax="0",
    total="100",
    items=[
        {"B1": "1", "B2": "美式咖啡", "B3": "2", "B5": "50", "B6": "100", "B7": "1", "B13": "1"},
    ],
)
# Response:
# {
#   "INDEX": {
#     "FUNCTIONCODE": "C0401",
#     "REPLY": "1",
#     "MESSAGE": "成功",
#     "INVOICENUMBER": "GS82775401",
#     "ERROR_CODE": "0000"
#   }
# }
```

### Example 5: Void an Invoice (C0501)

```python
from tools.b2c_invoice_tools import void_b2c_invoice

result = void_b2c_invoice(
    invoice_number="GS82775401",
    invoice_date="2026-04-01",
    buyer_id="0000000000",
    seller_id="23997652",
    cancel_date="2026-04-01",
    cancel_time="22:36:00",
    cancel_reason="測試作廢",
)
# Response:
# {
#   "INDEX": {
#     "FUNCTIONCODE": "C0501",
#     "REPLY": "1",
#     "MESSAGE": "成功",
#     "INVOICENUMBER": "GS82775401",
#     "ERROR_CODE": "0000"
#   }
# }
```

### Example 6: Query Cancel Status (Z11)

```python
from tools.query_tools import get_cancel_status

result = get_cancel_status(
    invoice_number="GS82775400",
    invoice_date="2026-04-01",
)
# Response:
# {
#   "INDEX": {
#     "FUNCTIONCODE": "Z11",
#     "REPLY": "1",
#     "STATUSCODE": "1",  ← 1=completed, 2=pending, 3=failed
#     "INVOICENUMBER": "GS82775400",
#     "ERROR_CODE": "0000"
#   }
# }
```

### Example 7: Full Workflow — Issue, Query, Void

A typical workflow: allocate numbers, create invoice, check status, void if needed.

```python
from tools.invoice_number_tools import get_invoice_numbers_expanded
from tools.b2c_invoice_tools import create_b2c_invoice, void_b2c_invoice

# Step 1: Get an available invoice number with AESKEY
numbers = get_invoice_numbers_expanded()
inv = numbers["INDEX"]["INVOICEDATA"][0]
# inv = {"INVOICE_NUMBER": "GS82775450", "AESKEY": "...", "RANDOMNUMBER": "7833"}

# Step 2: Create invoice using the allocated number
result = create_b2c_invoice(
    invoice_number=inv["INVOICE_NUMBER"],
    invoice_date="2026-04-01",
    invoice_time="14:30:00",
    buyer_id="0000000000",
    buyer_name="0000",
    invoice_type="07",
    donate_mark="0",
    print_mark="Y",
    random_number=inv["RANDOMNUMBER"],
    tax_type="1",
    tax_rate="0.05",
    tax_amount="10",
    sales_amount="190",
    free_tax="0",
    zero_tax="0",
    total="200",
    items=[
        {"B1": "1", "B2": "拿鐵咖啡", "B3": "2", "B5": "65", "B6": "130", "B7": "1", "B13": "1"},
        {"B1": "2", "B2": "巧克力蛋糕", "B3": "1", "B5": "70", "B6": "70", "B7": "2", "B13": "1"},
    ],
)
assert result["INDEX"]["REPLY"] == "1"

# Step 3: Void if needed
void_result = void_b2c_invoice(
    invoice_number=inv["INVOICE_NUMBER"],
    invoice_date="2026-04-01",
    buyer_id="0000000000",
    seller_id="23997652",
    cancel_date="2026-04-01",
    cancel_time="15:00:00",
    cancel_reason="客戶取消訂單",
)
assert void_result["INDEX"]["REPLY"] == "1"
```

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
