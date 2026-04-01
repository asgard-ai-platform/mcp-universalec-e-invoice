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
