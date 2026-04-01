# Changelog

## [0.1.0] - 2026-04-01

### Added
- 27 MCP tools covering all Universal EC e-invoice POS Web Service function codes (MIG4.1)
- Custom `einvoice_client.py` connector with INDEX/Invoice/Allowance wrapper support
- Environment-based configuration via `.env` (EINVOICE_BASE_URL, EINVOICE_SELLER_ID, EINVOICE_POS_ID, EINVOICE_POS_SN)
- 53 unit tests (mocked HTTP) + 5 regression tests (live API)
- Tool modules: system, invoice numbers, B2C invoices, B2B invoices, allowances, cancellation, queries, admin
- Claude Code integration (`.mcp.json`, `CLAUDE.md`)
