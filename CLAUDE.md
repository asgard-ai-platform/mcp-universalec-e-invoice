# MCP Universal EC E-Invoice Server

## Overview
MCP server wrapping the Universal EC (汎宇電商) Taiwan e-invoice POS Web Service (JSON, MIG4.1).
Exposes 27 tools covering all available function codes via stdio JSON-RPC 2.0.

## Setup
```bash
uv venv && source .venv/bin/activate
uv pip install -e ".[dev]"
cp .env.example .env  # then fill in your credentials
```

## Run
```bash
python mcp_server.py
```

## Test
```bash
# Unit tests (mocked, no credentials needed)
pytest tests/ --ignore=tests/test_regression.py -v

# Regression tests (requires .env with valid credentials)
pytest tests/test_regression.py -v -s
```

## Architecture

```
stdio (JSON-RPC 2.0)
  → mcp_server.py (entry point, side-effect imports trigger tool registration)
    → app.py (FastMCP singleton)
      → tools/*_tools.py (@mcp.tool() decorated functions)
        → connectors/einvoice_client.py (single POST connector)
          → config/settings.py (URL + credentials from .env)
```

### Tool Modules (27 tools)
| Module | Tools | Function Codes |
|---|---|---|
| system_tools.py | get_system_time | Y01 |
| invoice_number_tools.py | get_invoice_numbers, get_next_period_numbers, get_invoice_numbers_expanded, get_next_period_numbers_expanded | A01, C01, Z21, Z22 |
| b2c_invoice_tools.py | create_b2c_invoice, create_b2c_invoice_named, void_b2c_invoice | C0401, C0401N, C0501 |
| b2b_invoice_tools.py | create_b2b_invoice, void_b2b_invoice, create_b2b_exchange_invoice, void_b2b_exchange_invoice | A0401, A0501, A0101, A0201 |
| allowance_tools.py | create_b2c_allowance, create_b2c_allowance_named, void_b2c_allowance, create_b2b_allowance, void_b2b_allowance, create_b2b_exchange_allowance | D0401, D0401N, D0501, B0401, B0501, B0101 |
| cancel_tools.py | cancel_invoice, batch_cancel_invoice | C0701, B0701 |
| query_tools.py | get_cancel_status, get_downloaded_track_ranges, get_assignment_info, get_winning_list | Z11, Z31, Z33, Z34 |
| admin_tools.py | upload_next_period_tracks, assign_branch_tracks, report_unused_tracks | Z32, E0401, E0402 |

### Code Conventions
- English for all code, docstrings, and tool descriptions
- Use `connectors/einvoice_client.py` — don't call `requests` directly in tools
- All tools return `dict`
- Three JSON wrapper formats: INDEX (system/numbers), Invoice (CRUD), Allowance (B0501 only)
- Credentials from .env, injected by connector — never by tool code
