# Universal EC E-Invoice MCP Server Design

## Overview

MCP server wrapping the Universal EC (汎宇電商) Taiwan e-invoice POS Web Service (JSON format, MIG4.1). Exposes 27 MCP tools covering all available function codes via stdio JSON-RPC 2.0.

## API Characteristics

- **Single endpoint**: All requests POST to `GetInvoice.ashx`
- **Auth in body**: SELLERID, POSID, POSSN are part of the JSON payload (not HTTP headers)
- **Three wrapper formats**:
  - `{"INDEX": {...}}` — for system/number functions (A01, C01, Y01, Z21, Z22, Z11)
  - `{"Invoice": {...}}` — for invoice/allowance/admin CRUD (C0401, C0501, D0401, C0701, A0401, B0701, Z31-Z34, E-series, etc.)
  - `{"Allowance": {...}}` — for B0501 (void B2B allowance)
- **Content-Type**: `application/json; charset=utf-8`
- **HTTP Method**: POST only

## Environments

| Name | URL | Status |
|---|---|---|
| dev | `https://postest2.einvoice.com.tw/GetInvoice.ashx` | Connection refused |
| test | `https://epostw.einvoice.com.tw/GetInvoice.ashx` | Working (default) |
| production | `https://eposw.einvoice.com.tw/GetInvoice.ashx` | Requires production credentials |

## Configuration (`.env`)

```
EINVOICE_BASE_URL=https://epostw.einvoice.com.tw/GetInvoice.ashx
EINVOICE_SELLER_ID=23997652
EINVOICE_POS_ID=A002
EINVOICE_POS_SN=atzBZrjXQBRL1GPeq6Qq
```

## Architecture

```
stdio (JSON-RPC 2.0)
  -> mcp_server.py (imports all 8 tool modules)
    -> app.py (MCPServer "mcp-universalec-e-invoice")
      -> tools/
          system_tools.py          -- Y01
          invoice_number_tools.py  -- A01, C01, Z21, Z22
          b2c_invoice_tools.py     -- C0401, C0401N, C0501
          b2b_invoice_tools.py     -- A0401, A0501, A0101, A0201
          allowance_tools.py       -- D0401, D0401N, D0501, B0401, B0501, B0101
          cancel_tools.py          -- C0701, B0701
          query_tools.py           -- Z11, Z31, Z33, Z34
          admin_tools.py           -- Z32, E0401, E0402
        -> connectors/einvoice_client.py (single POST client)
          -> config/settings.py (URL + credentials from .env)
```

### Files to Remove (from template)

- **Entire `auth/` directory** — auth is embedded in JSON body, not HTTP headers
- `connectors/rest_client.py` — replaced by `einvoice_client.py`
- `connectors/graphql_client.py` — unused
- `connectors/mqtt_client.py` — unused
- `connectors/rss_client.py` — unused
- `connectors/scraper_client.py` — unused
- `tools/sample_tools.py` — replaced by 8 actual tool modules

### Files to Keep (from template)

- `app.py` — MCPServer singleton (rename service)
- `mcp_server.py` — entry point (update imports)
- `config/settings.py` — rewrite for einvoice config
- `connectors/__init__.py` — keep
- `tools/__init__.py` — keep
- `pyproject.toml` — update metadata

## Connector: `connectors/einvoice_client.py`

### Core Function

```python
def post_einvoice(function_code: str, payload: dict, wrapper: str = "INDEX") -> dict
```

- Auto-injects common fields: `SELLERID`, `POSID`, `POSSN`, `SYSTIME`
- Auto-injects default fields: `ACCOUNT="0000000000000000"`, `APPID="0000000000000000"`, `ServerType="invioce_ml"` (vendor typo is intentional)
- Wraps payload in `{"INDEX": {...}}`, `{"Invoice": {...}}`, or `{"Allowance": {...}}` based on `wrapper` param
- Sets `FUNCTIONCODE` (for INDEX) or `INVOICE_CODE`/`DISCOUNT_CODE` (for Invoice/Allowance) automatically
- SYSTIME format: `YYYY-MM-DD HH:mm:ss` for INDEX wrapper, `YYYY-MM-DD HH:mm:ss` for Invoice/Allowance wrapper
- Auto-injects credentials only at top level of wrapper; nested structures (e.g., Seller/Buyer info in B2B) are business parameters
- Retry with exponential backoff (3 attempts)
- Returns parsed JSON response dict
- Raises `EInvoiceAPIError` on failure

### Wrapper Mapping

| Wrapper | Function Codes |
|---|---|
| `INDEX` | A01, C01, Y01, Z21, Z22, Z11 |
| `Invoice` | C0401, C0401N, C0501, D0401, D0401N, D0501, C0701, A0401, A0501, A0101, A0201, B0401, B0101, B0701, Z31, Z32, Z33, Z34, E0401, E0402 |
| `Allowance` | B0501 |

### Structural Format Variants

- **C0401** uses positional field names (A1-A31, B1-B13, C1-C13, D1-D4) — flat key-value structure
- **C0401N / A0401 / A0101** use named fields in nested JSON (InvoiceNumber, Seller.Identifier, Details.ProductItem, etc.)
- **B0701** (batch cancel) re-submits full invoice data with cancellation info, not just invoice numbers
- **Z34** response includes `FILE_CONTENT` as a compressed binary blob — tool should return base64-encoded content

## MCP Tools (27 total)

### 1. `tools/system_tools.py` (1 tool)

| Tool | Function Code | Description |
|---|---|---|
| `get_system_time` | Y01 | Get server system time / connection test |

### 2. `tools/invoice_number_tools.py` (4 tools)

| Tool | Function Code | Description |
|---|---|---|
| `get_invoice_numbers` | A01 | Get invoice number allocation (current period) |
| `get_next_period_numbers` | C01 | Get invoice number allocation (next period) |
| `get_invoice_numbers_expanded` | Z21 | Get invoice numbers expanded per-invoice with AESKEY |
| `get_next_period_numbers_expanded` | Z22 | Get next period numbers expanded per-invoice with AESKEY |

### 3. `tools/b2c_invoice_tools.py` (3 tools)

| Tool | Function Code | Description |
|---|---|---|
| `create_b2c_invoice` | C0401 | Create B2C invoice (platform certified) |
| `create_b2c_invoice_n` | C0401N | Create B2C invoice (alternative format) |
| `void_b2c_invoice` | C0501 | Void a B2C invoice |

### 4. `tools/b2b_invoice_tools.py` (4 tools)

| Tool | Function Code | Description |
|---|---|---|
| `create_b2b_invoice` | A0401 | Create B2B invoice (platform certified) |
| `void_b2b_invoice` | A0501 | Void a B2B invoice |
| `create_b2b_exchange_invoice` | A0101 | Create B2B exchange invoice |
| `void_b2b_exchange_invoice` | A0201 | Void a B2B exchange invoice |

### 5. `tools/allowance_tools.py` (6 tools)

| Tool | Function Code | Description |
|---|---|---|
| `create_b2c_allowance` | D0401 | Create B2C allowance (折讓證明單) |
| `create_b2c_allowance_n` | D0401N | Create B2C allowance (alternative format) |
| `void_b2c_allowance` | D0501 | Void a B2C allowance |
| `create_b2b_allowance` | B0401 | Create B2B allowance |
| `void_b2b_allowance` | B0501 | Void a B2B allowance |
| `create_b2b_exchange_allowance` | B0101 | Create B2B exchange allowance |

### 6. `tools/cancel_tools.py` (2 tools)

| Tool | Function Code | Description |
|---|---|---|
| `cancel_invoice` | C0701 | Cancel (註銷) an invoice |
| `batch_cancel_invoice` | B0701 | Batch cancel invoices |

### 7. `tools/query_tools.py` (4 tools)

| Tool | Function Code | Description |
|---|---|---|
| `get_cancel_status` | Z11 | Get invoice cancel/void process status |
| `get_downloaded_track_ranges` | Z31 | Query downloaded invoice track ranges |
| `get_assignment_info` | Z33 | Query tax ID number assignment (auto/manual) |
| `download_winning_list` | Z34 | Download winning invoice list |

### 8. `tools/admin_tools.py` (3 tools)

| Tool | Function Code | Description |
|---|---|---|
| `upload_next_period_tracks` | Z32 | Upload next period invoice track numbers |
| `get_branch_assignment` | E0401 | Get branch office invoice number assignment |
| `get_unused_tracks` | E0402 | Get unused invoice track file |

## Tool Parameter Design

Each MCP tool exposes only the **business-relevant parameters** to the AI caller. Common/credential fields (SELLERID, POSID, POSSN, SYSTIME, ACCOUNT, APPID, ServerType) are injected by the connector.

Example — `create_b2c_invoice`:
- Required: `invoice_number`, `invoice_date`, `invoice_time`, `buyer_id`, `buyer_name`, `random_number`, `invoice_type`, `donate_mark`, `print_mark`, `tax_type`, `tax_rate`, `tax_amount`, `sales_amount`, `free_tax_amount`, `zero_tax_amount`, `total_amount`, `items` (list of line items)
- Optional: `carrier_type`, `carrier_id1`, `carrier_id2`, `donate_to`, `zero_tax_rate_reason`, `main_remark`, `customs_clearance_mark`, etc.

Line items structure:
- Required: `description`, `quantity`, `unit_price`, `amount`, `sequence_number`, `tax_type`
- Optional: `unit`, `remark`, `related_number`

## Error Handling

- `REPLY: "1"` = success
- `REPLY: "0"` = failure, `MESSAGE` contains error description
- `REPLY: "-1"` = validation failure (e.g., duplicate invoice, company suspended)
- `ERROR_CODE` field present in some responses (e.g., C0401, C0501) — codes include E002-E004, S010-S050, U010-U018 per vendor spec
- All tools return the full response dict for transparency
- Note: A0501 response returns `FUNCTIONCODE: "C0501"` (not "A0501") — a vendor API quirk
