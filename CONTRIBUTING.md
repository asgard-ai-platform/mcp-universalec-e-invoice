# Contributing

Thank you for contributing to the Universal EC E-Invoice MCP Server!

## Setup

```bash
git clone git@github.com:asgard-ai-platform/mcp-universalec-e-invoice.git
cd mcp-universalec-e-invoice
uv venv && source .venv/bin/activate
uv pip install -e ".[dev]"
cp .env.example .env
# Edit .env with your credentials
```

## Adding a New Tool

1. **Choose module**: Pick an existing file in `tools/` or create a new `tools/{domain}_tools.py`
2. **Import connector**: `from connectors.einvoice_client import post_einvoice`
3. **Write the tool**:
   ```python
   from app import mcp
   from connectors.einvoice_client import post_einvoice

   @mcp.tool()
   def my_new_tool(
       param: str = Field(description="What this param does"),
   ) -> dict:
       """What this tool does — shown in MCP tools/list."""
       return post_einvoice("FUNCTION_CODE", {"key": param}, wrapper="Invoice")
   ```
4. **Register**: If you created a new module, add `import tools.{module}  # noqa: F401` in `mcp_server.py`
5. **Test**: Add a test in `tests/test_{module}.py`

## Code Conventions

- English for code, docstrings, and tool descriptions
- Use `connectors/einvoice_client.py` — never call `requests` directly in tools
- All tools return `dict`
- Three JSON wrapper formats: `INDEX`, `Invoice`, `Allowance`
- Credentials from `.env`, injected by connector — never by tool code
- Use `Annotated[Optional[str], Field(...)] = None` for optional parameters

## Testing

```bash
# Unit tests (mocked, no credentials needed)
pytest tests/ --ignore=tests/test_regression.py -v

# Regression tests (requires .env with valid credentials)
pytest tests/test_regression.py -v -s
```

## Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/add-new-tool`
3. Write tests first (TDD)
4. Run full test suite
5. Submit a PR with a clear description
