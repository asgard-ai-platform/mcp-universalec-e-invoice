# Universal EC E-Invoice MCP Server Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build an MCP server wrapping all 27 Universal EC e-invoice API function codes, with unit tests (mocked HTTP) and regression tests (live test environment).

**Architecture:** Single POST endpoint connector (`einvoice_client.py`) supporting 3 wrapper formats (INDEX/Invoice/Allowance), with 8 tool modules organized by business function. TDD — write failing tests first, then implement.

**Tech Stack:** Python 3.10+, mcp SDK, requests, pytest, python-dotenv

**Spec:** `docs/superpowers/specs/2026-04-01-universalec-einvoice-mcp-design.md`

**Reference PDF:** `reference/汎宇電商電子發票POS機傳輸規格書_JSON_MIG4.1_20260101.pdf`

**Test environment:** `https://epostw.einvoice.com.tw/GetInvoice.ashx` (credentials in `reference/env_info.md`)

---

## File Structure

```
mcp-universalec-e-invoice/
├── .env.example                  # MODIFY: einvoice-specific vars
├── .env                          # CREATE: actual credentials (gitignored)
├── app.py                        # MODIFY: rename service
├── mcp_server.py                 # MODIFY: import 8 tool modules
├── pyproject.toml                # MODIFY: update metadata + deps
├── config/
│   ├── __init__.py               # KEEP
│   └── settings.py               # REWRITE: einvoice config from .env
├── connectors/
│   ├── __init__.py               # KEEP
│   └── einvoice_client.py        # CREATE: single POST connector
├── tools/
│   ├── __init__.py               # KEEP
│   ├── system_tools.py           # CREATE: Y01
│   ├── invoice_number_tools.py   # CREATE: A01, C01, Z21, Z22
│   ├── b2c_invoice_tools.py      # CREATE: C0401, C0401N, C0501
│   ├── b2b_invoice_tools.py      # CREATE: A0401, A0501, A0101, A0201
│   ├── allowance_tools.py        # CREATE: D0401, D0401N, D0501, B0401, B0501, B0101
│   ├── cancel_tools.py           # CREATE: C0701, B0701
│   ├── query_tools.py            # CREATE: Z11, Z31, Z33, Z34
│   └── admin_tools.py            # CREATE: Z32, E0401, E0402
├── tests/
│   ├── __init__.py               # CREATE
│   ├── conftest.py               # CREATE: shared fixtures, mock helpers
│   ├── test_einvoice_client.py   # CREATE: connector unit tests
│   ├── test_system_tools.py      # CREATE: Y01 unit tests
│   ├── test_invoice_number_tools.py  # CREATE
│   ├── test_b2c_invoice_tools.py     # CREATE
│   ├── test_b2b_invoice_tools.py     # CREATE
│   ├── test_allowance_tools.py       # CREATE
│   ├── test_cancel_tools.py          # CREATE
│   ├── test_query_tools.py           # CREATE
│   ├── test_admin_tools.py           # CREATE
│   └── test_regression.py        # CREATE: live API integration tests
├── DELETE: auth/ (entire directory)
├── DELETE: connectors/rest_client.py
├── DELETE: connectors/graphql_client.py
├── DELETE: connectors/mqtt_client.py
├── DELETE: connectors/rss_client.py
├── DELETE: connectors/scraper_client.py
├── DELETE: tools/sample_tools.py
├── DELETE: tests/test_all_tools.py
├── DELETE: scripts/auth/test_connection.py
```

---

### Task 1: Project cleanup and foundation

**Files:**
- Delete: `auth/__init__.py`, `auth/bearer.py`, `auth/api_key.py`, `auth/oauth2.py`, `auth/none.py`
- Delete: `connectors/rest_client.py`, `connectors/graphql_client.py`, `connectors/mqtt_client.py`, `connectors/rss_client.py`, `connectors/scraper_client.py`
- Delete: `tools/sample_tools.py`, `tests/test_all_tools.py`, `scripts/auth/test_connection.py`
- Modify: `.env.example`, `app.py`, `pyproject.toml`
- Create: `.env`, `tests/__init__.py`, `tests/conftest.py`

- [ ] **Step 1: Delete unused template files**

```bash
rm -rf auth/
rm connectors/rest_client.py connectors/graphql_client.py connectors/mqtt_client.py connectors/rss_client.py connectors/scraper_client.py
rm tools/sample_tools.py
rm -f tests/test_all_tools.py
rm -rf scripts/
```

- [ ] **Step 2: Update `.env.example`**

```
# Universal EC E-Invoice API Configuration
EINVOICE_BASE_URL=https://epostw.einvoice.com.tw/GetInvoice.ashx
EINVOICE_SELLER_ID=your_seller_id
EINVOICE_POS_ID=your_pos_id
EINVOICE_POS_SN=your_pos_sn
```

- [ ] **Step 3: Create `.env` with test credentials**

```
EINVOICE_BASE_URL=https://epostw.einvoice.com.tw/GetInvoice.ashx
EINVOICE_SELLER_ID=23997652
EINVOICE_POS_ID=A002
EINVOICE_POS_SN=atzBZrjXQBRL1GPeq6Qq
```

- [ ] **Step 4: Update `app.py`**

```python
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("mcp-universalec-e-invoice", version="0.1.0")
```

- [ ] **Step 5: Update `pyproject.toml`**

```toml
[build-system]
requires = ["setuptools>=68.0"]
build-backend = "setuptools.backends._legacy:_Backend"

[project]
name = "mcp-universalec-e-invoice"
version = "0.1.0"
description = "MCP Server for Universal EC E-Invoice — Taiwan e-invoice POS Web Service"
readme = "README.md"
license = {text = "MIT"}
requires-python = ">=3.10"
authors = [
    {name = "Asgard AI Platform", email = "dev@asgard.ai"},
]

dependencies = [
    "requests>=2.31.0",
    "mcp>=1.0.0",
    "python-dotenv>=1.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-mock>=3.10.0",
]

[project.scripts]
mcp-universalec-e-invoice = "mcp_server:main"

[tool.setuptools]
py-modules = ["mcp_server", "app"]

[tool.setuptools.packages.find]
include = ["config*", "connectors*", "tools*"]
```

- [ ] **Step 6: Create `tests/__init__.py` and `tests/conftest.py`**

`tests/__init__.py`: empty file

`tests/conftest.py`:
```python
import os
import pytest

# Ensure test env vars are set for unit tests (mocked - don't need real creds)
@pytest.fixture(autouse=True)
def mock_env(monkeypatch):
    monkeypatch.setenv("EINVOICE_BASE_URL", "https://test.example.com/GetInvoice.ashx")
    monkeypatch.setenv("EINVOICE_SELLER_ID", "12345678")
    monkeypatch.setenv("EINVOICE_POS_ID", "T001")
    monkeypatch.setenv("EINVOICE_POS_SN", "test_possn_key_123")


@pytest.fixture
def mock_post_success(mocker):
    """Mock requests.post returning a successful Y01 response."""
    mock_resp = mocker.Mock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "INDEX": {
            "FUNCTIONCODE": "Y01",
            "REPLY": "1",
            "MESSAGE": "連線成功",
        }
    }
    return mocker.patch("connectors.einvoice_client.requests.post", return_value=mock_resp)


@pytest.fixture
def mock_post_failure(mocker):
    """Mock requests.post returning a failure response."""
    mock_resp = mocker.Mock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "INDEX": {
            "FUNCTIONCODE": "Y01",
            "REPLY": "0",
            "MESSAGE": "失敗請確認POS機已註冊且無停用",
        }
    }
    return mocker.patch("connectors.einvoice_client.requests.post", return_value=mock_resp)
```

- [ ] **Step 7: Commit**

```bash
git add -A
git commit -m "chore: clean up template files and configure project for Universal EC e-invoice"
```

---

### Task 2: Config settings module

**Files:**
- Rewrite: `config/settings.py`
- Test: `tests/test_einvoice_client.py` (settings portion)

- [ ] **Step 1: Write failing test for settings**

`tests/test_einvoice_client.py`:
```python
import os
from config.settings import get_base_url, get_credentials


def test_get_base_url(mock_env):
    assert get_base_url() == "https://test.example.com/GetInvoice.ashx"


def test_get_credentials(mock_env):
    creds = get_credentials()
    assert creds["SELLERID"] == "12345678"
    assert creds["POSID"] == "T001"
    assert creds["POSSN"] == "test_possn_key_123"


def test_get_credentials_missing_env(monkeypatch):
    monkeypatch.delenv("EINVOICE_SELLER_ID", raising=False)
    monkeypatch.delenv("EINVOICE_POS_ID", raising=False)
    monkeypatch.delenv("EINVOICE_POS_SN", raising=False)
    import pytest
    with pytest.raises(RuntimeError, match="EINVOICE_SELLER_ID"):
        get_credentials()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /Users/williamwang/Documents/executing/asgard-opensource/mcp-universalec-e-invoice && python -m pytest tests/test_einvoice_client.py -v`
Expected: FAIL — `get_base_url` / `get_credentials` not found

- [ ] **Step 3: Implement `config/settings.py`**

```python
import os
from dotenv import load_dotenv

load_dotenv()


def get_base_url() -> str:
    url = os.environ.get("EINVOICE_BASE_URL")
    if not url:
        raise RuntimeError(
            "Missing EINVOICE_BASE_URL. Set it in .env or environment.\n"
            "  Example: EINVOICE_BASE_URL=https://epostw.einvoice.com.tw/GetInvoice.ashx"
        )
    return url


def get_credentials() -> dict:
    seller_id = os.environ.get("EINVOICE_SELLER_ID")
    pos_id = os.environ.get("EINVOICE_POS_ID")
    pos_sn = os.environ.get("EINVOICE_POS_SN")
    if not seller_id:
        raise RuntimeError("Missing EINVOICE_SELLER_ID environment variable.")
    if not pos_id:
        raise RuntimeError("Missing EINVOICE_POS_ID environment variable.")
    if not pos_sn:
        raise RuntimeError("Missing EINVOICE_POS_SN environment variable.")
    return {
        "SELLERID": seller_id,
        "POSID": pos_id,
        "POSSN": pos_sn,
    }
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_einvoice_client.py::test_get_base_url tests/test_einvoice_client.py::test_get_credentials tests/test_einvoice_client.py::test_get_credentials_missing_env -v`
Expected: 3 PASSED

- [ ] **Step 5: Commit**

```bash
git add config/settings.py tests/test_einvoice_client.py
git commit -m "feat: add config/settings.py with env-based einvoice configuration"
```

---

### Task 3: E-Invoice connector

**Files:**
- Create: `connectors/einvoice_client.py`
- Extend: `tests/test_einvoice_client.py`

- [ ] **Step 1: Write failing tests for connector**

Append to `tests/test_einvoice_client.py`:
```python
import json
from connectors.einvoice_client import post_einvoice, EInvoiceAPIError


class TestPostEinvoiceIndexWrapper:
    def test_index_wrapper_sets_functioncode(self, mocker, mock_env):
        mock_resp = mocker.Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"INDEX": {"FUNCTIONCODE": "Y01", "REPLY": "1", "MESSAGE": "連線成功"}}
        mock_post = mocker.patch("connectors.einvoice_client.requests.post", return_value=mock_resp)

        result = post_einvoice("Y01", {})
        called_body = json.loads(mock_post.call_args[1]["data"])
        assert "INDEX" in called_body
        assert called_body["INDEX"]["FUNCTIONCODE"] == "Y01"
        assert called_body["INDEX"]["SELLERID"] == "12345678"
        assert called_body["INDEX"]["POSID"] == "T001"
        assert called_body["INDEX"]["POSSN"] == "test_possn_key_123"
        assert result["INDEX"]["REPLY"] == "1"

    def test_index_wrapper_injects_defaults(self, mocker, mock_env):
        mock_resp = mocker.Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"INDEX": {"REPLY": "1"}}
        mock_post = mocker.patch("connectors.einvoice_client.requests.post", return_value=mock_resp)

        post_einvoice("A01", {})
        called_body = json.loads(mock_post.call_args[1]["data"])
        assert called_body["INDEX"]["ACCOUNT"] == "0000000000000000"
        assert called_body["INDEX"]["APPID"] == "0000000000000000"
        assert called_body["INDEX"]["ServerType"] == "invioce_ml"


class TestPostEinvoiceInvoiceWrapper:
    def test_invoice_wrapper_sets_invoice_code(self, mocker, mock_env):
        mock_resp = mocker.Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"INDEX": {"FUNCTIONCODE": "C0401", "REPLY": "1"}}
        mock_post = mocker.patch("connectors.einvoice_client.requests.post", return_value=mock_resp)

        post_einvoice("C0401", {"A1": "C0401", "A2": "AB12345678"}, wrapper="Invoice")
        called_body = json.loads(mock_post.call_args[1]["data"])
        assert "Invoice" in called_body
        assert called_body["Invoice"]["A1"] == "C0401"


class TestPostEinvoiceAllowanceWrapper:
    def test_allowance_wrapper(self, mocker, mock_env):
        mock_resp = mocker.Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"INDEX": {"FUNCTIONCODE": "B0501", "REPLY": "1"}}
        mock_post = mocker.patch("connectors.einvoice_client.requests.post", return_value=mock_resp)

        post_einvoice("B0501", {"INVOICE_CODE": "B0501"}, wrapper="Allowance")
        called_body = json.loads(mock_post.call_args[1]["data"])
        assert "Allowance" in called_body


class TestPostEinvoiceErrorHandling:
    def test_http_error_raises(self, mocker, mock_env):
        mock_resp = mocker.Mock()
        mock_resp.status_code = 500
        mock_resp.text = "Internal Server Error"
        mocker.patch("connectors.einvoice_client.requests.post", return_value=mock_resp)

        import pytest
        with pytest.raises(EInvoiceAPIError, match="500"):
            post_einvoice("Y01", {})

    def test_connection_error_retries(self, mocker, mock_env):
        import requests as req
        mock_post = mocker.patch(
            "connectors.einvoice_client.requests.post",
            side_effect=req.exceptions.ConnectionError("refused"),
        )
        import pytest
        with pytest.raises(EInvoiceAPIError, match="retries"):
            post_einvoice("Y01", {}, retries=2)
        assert mock_post.call_count == 2
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_einvoice_client.py -v`
Expected: FAIL — `post_einvoice`, `EInvoiceAPIError` not found

- [ ] **Step 3: Implement `connectors/einvoice_client.py`**

```python
"""Universal EC E-Invoice API connector — single POST endpoint."""

import json
import time
from datetime import datetime

import requests

from config.settings import get_base_url, get_credentials


class EInvoiceAPIError(Exception):
    def __init__(self, status_code: int, message: str, function_code: str = ""):
        self.status_code = status_code
        self.message = message
        self.function_code = function_code
        super().__init__(f"[{status_code}] {function_code}: {message}")


def _get_systime() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def post_einvoice(
    function_code: str,
    payload: dict,
    wrapper: str = "INDEX",
    retries: int = 3,
    timeout: int = 60,
) -> dict:
    """Post a request to the Universal EC e-invoice API.

    Args:
        function_code: The API function code (e.g., "Y01", "C0401").
        payload: Business-specific fields for this function.
        wrapper: Wrapper format — "INDEX", "Invoice", or "Allowance".
        retries: Number of retry attempts for transient errors.
        timeout: Request timeout in seconds.

    Returns:
        Parsed JSON response dict.

    Raises:
        EInvoiceAPIError: On HTTP errors or after all retries exhausted.
    """
    url = get_base_url()
    creds = get_credentials()

    if wrapper == "INDEX":
        body = {
            "INDEX": {
                "FUNCTIONCODE": function_code,
                "SELLERID": creds["SELLERID"],
                "POSID": creds["POSID"],
                "POSSN": creds["POSSN"],
                "SYSTIME": _get_systime(),
                "ACCOUNT": "0000000000000000",
                "APPID": "0000000000000000",
                "ServerType": "invioce_ml",
                "REPLY": "",
                "MESSAGE": "",
                "VERIONUPDATE": "",
                "EcrId": "",
                "APPVSERION": "",
                **payload,
            }
        }
    elif wrapper == "Invoice":
        inner = {
            "POSSN": creds["POSSN"],
            "POSID": creds["POSID"],
            "SELLERID": creds["SELLERID"],
            "SYSTIME": _get_systime(),
            "ACCOUNT": "0000000000000000",
            "APPID": "0000000000000000",
            "ServerType": "invioce_ml",
            **payload,
        }
        body = {"Invoice": inner}
    elif wrapper == "Allowance":
        inner = {
            "POSSN": creds["POSSN"],
            "POSID": creds["POSID"],
            "SELLERID": creds["SELLERID"],
            "SYSTIME": _get_systime(),
            **payload,
        }
        body = {"Allowance": inner}
    else:
        raise ValueError(f"Unknown wrapper type: {wrapper}")

    headers = {"Content-Type": "application/json; charset=utf-8"}

    for attempt in range(retries):
        try:
            response = requests.post(
                url,
                data=json.dumps(body, ensure_ascii=False),
                headers=headers,
                timeout=timeout,
            )
            if response.status_code >= 400:
                raise EInvoiceAPIError(
                    status_code=response.status_code,
                    message=response.text[:500],
                    function_code=function_code,
                )
            return response.json()

        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
            else:
                raise EInvoiceAPIError(
                    status_code=0,
                    message="Request failed after all retries (timeout/connection error)",
                    function_code=function_code,
                )
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m pytest tests/test_einvoice_client.py -v`
Expected: ALL PASSED

- [ ] **Step 5: Commit**

```bash
git add connectors/einvoice_client.py tests/test_einvoice_client.py
git commit -m "feat: add einvoice_client.py connector with INDEX/Invoice/Allowance wrappers"
```

---

### Task 4: System tools (Y01)

**Files:**
- Create: `tools/system_tools.py`
- Create: `tests/test_system_tools.py`

- [ ] **Step 1: Write failing test**

`tests/test_system_tools.py`:
```python
import json


def test_get_system_time(mocker, mock_env):
    mock_resp = mocker.Mock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "INDEX": {
            "FUNCTIONCODE": "Y01",
            "REPLY": "1",
            "MESSAGE": "連線成功",
            "SYSTIME": "2026/04/01 21:30:20",
            "POSID": "T001",
            "SELLERID": "12345678",
        }
    }
    mocker.patch("connectors.einvoice_client.requests.post", return_value=mock_resp)

    from tools.system_tools import get_system_time
    result = get_system_time()
    assert result["INDEX"]["REPLY"] == "1"
    assert result["INDEX"]["MESSAGE"] == "連線成功"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_system_tools.py -v`
Expected: FAIL

- [ ] **Step 3: Implement `tools/system_tools.py`**

```python
"""System tools — Y01 get system time / connection test."""

from app import mcp
from connectors.einvoice_client import post_einvoice


@mcp.tool()
def get_system_time() -> dict:
    """Get the e-invoice server system time. Also serves as a connection test (Y01)."""
    return post_einvoice("Y01", {})
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_system_tools.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tools/system_tools.py tests/test_system_tools.py
git commit -m "feat: add Y01 get_system_time tool"
```

---

### Task 5: Invoice number tools (A01, C01, Z21, Z22)

**Files:**
- Create: `tools/invoice_number_tools.py`
- Create: `tests/test_invoice_number_tools.py`

- [ ] **Step 1: Write failing tests**

`tests/test_invoice_number_tools.py`:
```python
import json


class TestGetInvoiceNumbers:
    def test_a01_basic(self, mocker, mock_env):
        mock_resp = mocker.Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "INDEX": {
                "FUNCTIONCODE": "A01",
                "REPLY": "1",
                "MESSAGE": "成功",
                "TAXMONTH": "10708",
                "INVOICEHEADER": "DC",
                "INVOICESTART": "51705750",
                "INVOICEEND": "51705799",
                "QRCodeASKey": "5F2BF5EEA62517788999A08024437",
                "TYPE": "03",
            }
        }
        mock_post = mocker.patch("connectors.einvoice_client.requests.post", return_value=mock_resp)

        from tools.invoice_number_tools import get_invoice_numbers
        result = get_invoice_numbers()
        assert result["INDEX"]["REPLY"] == "1"
        assert result["INDEX"]["INVOICEHEADER"] == "DC"

        called_body = json.loads(mock_post.call_args[1]["data"])
        assert called_body["INDEX"]["FUNCTIONCODE"] == "A01"


class TestGetNextPeriodNumbers:
    def test_c01_basic(self, mocker, mock_env):
        mock_resp = mocker.Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "INDEX": {"FUNCTIONCODE": "C01", "REPLY": "1", "INVOICEHEADER": "KK"}
        }
        mock_post = mocker.patch("connectors.einvoice_client.requests.post", return_value=mock_resp)

        from tools.invoice_number_tools import get_next_period_numbers
        result = get_next_period_numbers()
        called_body = json.loads(mock_post.call_args[1]["data"])
        assert called_body["INDEX"]["FUNCTIONCODE"] == "C01"
        assert result["INDEX"]["REPLY"] == "1"


class TestGetInvoiceNumbersExpanded:
    def test_z21_basic(self, mocker, mock_env):
        mock_resp = mocker.Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "INDEX": {
                "FUNCTIONCODE": "Z21",
                "REPLY": "1",
                "INVOICEDATA": [
                    {"INVOICE_NUMBER": "BX00000000", "AESKEY": "abc==", "RANDOMNUMBER": "1234", "TAXMONTH": "10806"}
                ],
            }
        }
        mock_post = mocker.patch("connectors.einvoice_client.requests.post", return_value=mock_resp)

        from tools.invoice_number_tools import get_invoice_numbers_expanded
        result = get_invoice_numbers_expanded()
        called_body = json.loads(mock_post.call_args[1]["data"])
        assert called_body["INDEX"]["FUNCTIONCODE"] == "Z21"
        assert len(result["INDEX"]["INVOICEDATA"]) == 1


class TestGetNextPeriodNumbersExpanded:
    def test_z22_basic(self, mocker, mock_env):
        mock_resp = mocker.Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "INDEX": {"FUNCTIONCODE": "Z22", "REPLY": "1", "INVOICEDATA": []}
        }
        mock_post = mocker.patch("connectors.einvoice_client.requests.post", return_value=mock_resp)

        from tools.invoice_number_tools import get_next_period_numbers_expanded
        result = get_next_period_numbers_expanded()
        called_body = json.loads(mock_post.call_args[1]["data"])
        assert called_body["INDEX"]["FUNCTIONCODE"] == "Z22"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_invoice_number_tools.py -v`
Expected: FAIL

- [ ] **Step 3: Implement `tools/invoice_number_tools.py`**

```python
"""Invoice number tools — A01, C01, Z21, Z22."""

from typing import Optional
from pydantic import Field
from app import mcp
from connectors.einvoice_client import post_einvoice


@mcp.tool()
def get_invoice_numbers(
    tax_month: Optional[str] = Field(default=None, description="Invoice period (YYMM, e.g. '11304'). If empty, gets current period."),
    invoice_header: Optional[str] = Field(default=None, description="Invoice track (2 uppercase letters, e.g. 'DC'). If empty, auto-assigned."),
) -> dict:
    """Get invoice number allocation for the current period (A01). Returns track, start/end numbers, and QRCode AES key."""
    payload = {}
    if tax_month:
        payload["TAXMONTH"] = tax_month
    if invoice_header:
        payload["INVOICEHEADER"] = invoice_header
    return post_einvoice("A01", payload)


@mcp.tool()
def get_next_period_numbers(
    tax_month: Optional[str] = Field(default=None, description="Invoice period (YYMM). If empty, gets next period."),
    invoice_header: Optional[str] = Field(default=None, description="Invoice track (2 uppercase letters)."),
) -> dict:
    """Get invoice number allocation for the next period (C01). Returns track, start/end numbers, and QRCode AES key."""
    payload = {}
    if tax_month:
        payload["TAXMONTH"] = tax_month
    if invoice_header:
        payload["INVOICEHEADER"] = invoice_header
    return post_einvoice("C01", payload)


@mcp.tool()
def get_invoice_numbers_expanded(
    tax_month: Optional[str] = Field(default=None, description="Invoice period (YYMM)."),
    invoice_header: Optional[str] = Field(default=None, description="Invoice track (2 uppercase letters)."),
) -> dict:
    """Get invoice numbers expanded per-invoice with AESKEY for current period (Z21). Returns INVOICEDATA array with individual invoice numbers, AESKEY, and random numbers."""
    payload = {}
    if tax_month:
        payload["TAXMONTH"] = tax_month
    if invoice_header:
        payload["INVOICEHEADER"] = invoice_header
    return post_einvoice("Z21", payload)


@mcp.tool()
def get_next_period_numbers_expanded(
    tax_month: Optional[str] = Field(default=None, description="Invoice period (YYMM)."),
    invoice_header: Optional[str] = Field(default=None, description="Invoice track (2 uppercase letters)."),
) -> dict:
    """Get invoice numbers expanded per-invoice with AESKEY for next period (Z22). Returns INVOICEDATA array with individual invoice numbers, AESKEY, and random numbers."""
    payload = {}
    if tax_month:
        payload["TAXMONTH"] = tax_month
    if invoice_header:
        payload["INVOICEHEADER"] = invoice_header
    return post_einvoice("Z22", payload)
```

- [ ] **Step 4: Run tests**

Run: `python -m pytest tests/test_invoice_number_tools.py -v`
Expected: ALL PASSED

- [ ] **Step 5: Commit**

```bash
git add tools/invoice_number_tools.py tests/test_invoice_number_tools.py
git commit -m "feat: add invoice number tools (A01, C01, Z21, Z22)"
```

---

### Task 6: B2C invoice tools (C0401, C0401N, C0501)

**Files:**
- Create: `tools/b2c_invoice_tools.py`
- Create: `tests/test_b2c_invoice_tools.py`

- [ ] **Step 1: Write failing tests**

`tests/test_b2c_invoice_tools.py`:
```python
import json


class TestCreateB2CInvoice:
    """C0401 — positional field format (A1-A31, B1-B13, C1-C13, D1-D4)."""

    def test_c0401_payload_structure(self, mocker, mock_env):
        mock_resp = mocker.Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"INDEX": {"FUNCTIONCODE": "C0401", "REPLY": "1", "MESSAGE": "成功", "ERROR_CODE": "0000"}}
        mock_post = mocker.patch("connectors.einvoice_client.requests.post", return_value=mock_resp)

        from tools.b2c_invoice_tools import create_b2c_invoice
        result = create_b2c_invoice(
            invoice_number="DC51094165",
            invoice_date="2018-06-13",
            invoice_time="09:49:00",
            buyer_id="0000000000",
            buyer_name="0000",
            invoice_type="03",
            donate_mark="0",
            print_mark="N",
            random_number="0632",
            tax_type="1",
            tax_rate="0.05",
            tax_amount="0",
            sales_amount="30",
            free_tax_amount="0",
            zero_tax_amount="0",
            total_amount="30",
            items=[
                {"description": "麵包 10 元", "quantity": "1.000", "unit_price": "10", "amount": "10", "sequence_number": "1", "tax_type": "1"},
            ],
        )
        called_body = json.loads(mock_post.call_args[1]["data"])
        assert "Invoice" in called_body
        inv = called_body["Invoice"]
        assert inv["A1"] == "C0401"
        assert inv["A2"] == "DC51094165"
        assert inv["A22"] == "03"
        assert inv["A24"] == "0"
        assert inv["A30"] == "0632"
        assert inv["C4"] == "1"
        assert inv["C7"] == "30"
        assert len(inv["B"]) == 1
        assert inv["B"][0]["B2"] == "麵包 10 元"
        assert result["INDEX"]["REPLY"] == "1"


class TestCreateB2CInvoiceN:
    """C0401N — named field format (nested Main/Details/Amount)."""

    def test_c0401n_payload_structure(self, mocker, mock_env):
        mock_resp = mocker.Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"INDEX": {"FUNCTIONCODE": "C0401N", "REPLY": "1", "ERROR_CODE": "0000"}}
        mock_post = mocker.patch("connectors.einvoice_client.requests.post", return_value=mock_resp)

        from tools.b2c_invoice_tools import create_b2c_invoice_n
        result = create_b2c_invoice_n(
            invoice_number="AB01234567",
            invoice_date="2022-02-22",
            invoice_time="10:18:10",
            seller_id="23997652",
            buyer_id="0000000000",
            buyer_name="0000",
            invoice_type="07",
            donate_mark="0",
            print_mark="Y",
            random_number="1234",
            tax_type="1",
            tax_rate="0.05",
            tax_amount="0",
            sales_amount="250",
            free_tax_sales_amount="0",
            zero_tax_sales_amount="0",
            total_amount="250",
            items=[
                {"description": "飲料", "quantity": "1", "unit_price": "50", "tax_type": "1", "amount": "50", "sequence_number": "1"},
            ],
        )
        called_body = json.loads(mock_post.call_args[1]["data"])
        assert "Invoice" in called_body
        inv = called_body["Invoice"]
        assert inv["INVOICE_CODE"] == "C0401N"
        assert inv["Main"]["InvoiceNumber"] == "AB01234567"
        assert inv["Details"]["ProductItem"][0]["Description"] == "飲料"
        assert inv["Amount"]["TotalAmount"] == "250"


class TestVoidB2CInvoice:
    """C0501 — void a B2C invoice."""

    def test_c0501_payload(self, mocker, mock_env):
        mock_resp = mocker.Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"INDEX": {"FUNCTIONCODE": "C0501", "REPLY": "1", "ERROR_CODE": "0000"}}
        mock_post = mocker.patch("connectors.einvoice_client.requests.post", return_value=mock_resp)

        from tools.b2c_invoice_tools import void_b2c_invoice
        result = void_b2c_invoice(
            invoice_number="FF69780401",
            invoice_date="2018-07-11",
            buyer_id="0000000000",
            seller_id="23997652",
            cancel_date="2018-07-11",
            cancel_time="10:08:56",
            cancel_reason="系統作廢",
        )
        called_body = json.loads(mock_post.call_args[1]["data"])
        assert "Invoice" in called_body
        inv = called_body["Invoice"]
        assert inv["INVOICE_CODE"] == "C0501"
        assert inv["INVOICE_NUMBER"] == "FF69780401"
        assert inv["CANCEL_REASON"] == "系統作廢"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_b2c_invoice_tools.py -v`
Expected: FAIL

- [ ] **Step 3: Implement `tools/b2c_invoice_tools.py`**

```python
"""B2C invoice tools — C0401, C0401N, C0501."""

from typing import Optional
from pydantic import Field
from app import mcp
from connectors.einvoice_client import post_einvoice


@mcp.tool()
def create_b2c_invoice(
    invoice_number: str = Field(description="Invoice number (10 chars, e.g. 'DC51094165')"),
    invoice_date: str = Field(description="Invoice date (yyyy-mm-dd)"),
    invoice_time: str = Field(description="Invoice time (HH:mm:ss)"),
    buyer_id: str = Field(description="Buyer tax ID (10 digits, '0000000000' for consumers)"),
    buyer_name: str = Field(description="Buyer name ('0000' auto-converts to 4 random digits)"),
    invoice_type: str = Field(description="Invoice type code (e.g. '03', '07')"),
    donate_mark: str = Field(description="Donation mark: '0'=no, '1'=yes"),
    print_mark: str = Field(description="Paper print mark: 'Y' or 'N'"),
    random_number: str = Field(description="4-digit random number for anti-forgery"),
    tax_type: str = Field(description="Tax type: '1'=taxable, '2'=zero-rate, '3'=tax-free, '9'=mixed"),
    tax_rate: str = Field(description="Tax rate (e.g. '0.05' for 5%)"),
    tax_amount: str = Field(description="Tax amount (integer, rounded)"),
    sales_amount: str = Field(description="Taxable sales amount (integer)"),
    free_tax_amount: str = Field(description="Tax-free sales amount ('0' if none)"),
    zero_tax_amount: str = Field(description="Zero-tax sales amount ('0' if none)"),
    total_amount: str = Field(description="Total amount including tax (integer)"),
    items: list = Field(description="Line items: list of {description, quantity, unit_price, amount, sequence_number, tax_type}. Optional: unit, remark, related_number."),
    carrier_type: Optional[str] = Field(default=None, description="Carrier type code"),
    carrier_id1: Optional[str] = Field(default=None, description="Carrier visible ID (外碼)"),
    carrier_id2: Optional[str] = Field(default=None, description="Carrier hidden ID (內碼)"),
    donate_to: Optional[str] = Field(default=None, description="Donation recipient tax ID or love code"),
    zero_tax_rate_reason: Optional[str] = Field(default=None, description="Zero tax rate reason code (required when tax_type='2')"),
    main_remark: Optional[str] = Field(default=None, description="General remark"),
    customs_clearance_mark: Optional[str] = Field(default=None, description="Customs clearance mark"),
    discount_amount: Optional[str] = Field(default=None, description="Discount amount"),
    currency: Optional[str] = Field(default=None, description="Currency code for foreign currency"),
    exchange_rate: Optional[str] = Field(default=None, description="Exchange rate"),
    original_currency_amount: Optional[str] = Field(default=None, description="Original currency amount"),
) -> dict:
    """Create a B2C invoice using positional field format (C0401). Fields use A1-A31, B1-B13, C1-C13, D1-D4 naming."""
    b_items = []
    for item in items:
        b = {
            "B1": item.get("sequence_number", "1"),
            "B2": item["description"],
            "B3": item["quantity"],
            "B5": item["unit_price"],
            "B6": item["amount"],
            "B7": item.get("sequence_number", "1"),
            "B13": item.get("tax_type", "1"),
        }
        if item.get("unit"):
            b["B4"] = item["unit"]
        if item.get("remark"):
            b["B8"] = item["remark"]
        if item.get("related_number"):
            b["B9"] = item["related_number"]
        b_items.append(b)

    payload = {
        "A1": "C0401",
        "A2": invoice_number,
        "A3": invoice_date,
        "A4": invoice_time,
        "A5": buyer_id,
        "A6": buyer_name,
        "A22": invoice_type,
        "A24": donate_mark,
        "A28": print_mark,
        "A30": random_number,
        "B": b_items,
        "C1": sales_amount,
        "C2": free_tax_amount,
        "C3": zero_tax_amount,
        "C4": tax_type,
        "C5": tax_rate,
        "C6": tax_amount,
        "C7": total_amount,
    }

    if carrier_type:
        payload["A25"] = carrier_type
    if carrier_id1:
        payload["A26"] = carrier_id1
    if carrier_id2:
        payload["A27"] = carrier_id2
    if donate_to:
        payload["A29"] = donate_to
    if zero_tax_rate_reason:
        payload["A31"] = zero_tax_rate_reason
    if main_remark:
        payload["A16"] = main_remark
    if customs_clearance_mark:
        payload["A17"] = customs_clearance_mark
    if discount_amount:
        payload["C8"] = discount_amount
    if currency:
        payload["C11"] = currency
    if exchange_rate:
        payload["C10"] = exchange_rate
    if original_currency_amount:
        payload["C9"] = original_currency_amount

    return post_einvoice("C0401", payload, wrapper="Invoice")


@mcp.tool()
def create_b2c_invoice_n(
    invoice_number: str = Field(description="Invoice number (10 chars)"),
    invoice_date: str = Field(description="Invoice date (yyyy-mm-dd)"),
    invoice_time: str = Field(description="Invoice time (HH:mm:ss)"),
    seller_id: str = Field(description="Seller tax ID (8 digits)"),
    buyer_id: str = Field(description="Buyer tax ID ('0000000000' for consumers)"),
    buyer_name: str = Field(description="Buyer name"),
    invoice_type: str = Field(description="Invoice type code"),
    donate_mark: str = Field(description="Donation mark: '0'=no, '1'=yes"),
    print_mark: str = Field(description="Paper print mark: 'Y' or 'N'"),
    random_number: str = Field(description="4-digit random number"),
    tax_type: str = Field(description="Tax type: '1'=taxable, '2'=zero, '3'=free, '9'=mixed"),
    tax_rate: str = Field(description="Tax rate (e.g. '0.05')"),
    tax_amount: str = Field(description="Tax amount"),
    sales_amount: str = Field(description="Taxable sales amount"),
    free_tax_sales_amount: str = Field(description="Free-tax sales amount ('0' if none)"),
    zero_tax_sales_amount: str = Field(description="Zero-tax sales amount ('0' if none)"),
    total_amount: str = Field(description="Total amount"),
    items: list = Field(description="Line items: list of {description, quantity, unit_price, tax_type, amount, sequence_number}"),
    carrier_type: Optional[str] = Field(default=None, description="Carrier type code"),
    carrier_id1: Optional[str] = Field(default=None, description="Carrier visible ID"),
    carrier_id2: Optional[str] = Field(default=None, description="Carrier hidden ID"),
    npo_ban: Optional[str] = Field(default=None, description="NPO tax ID for donation"),
    zero_tax_rate_reason: Optional[str] = Field(default=None, description="Zero tax rate reason"),
    main_remark: Optional[str] = Field(default=None, description="General remark"),
) -> dict:
    """Create a B2C invoice using named field format (C0401N). Uses nested Main/Details/Amount structure."""
    product_items = []
    for item in items:
        pi = {
            "Description": item["description"],
            "Quantity": item["quantity"],
            "UnitPrice": item["unit_price"],
            "TaxType": item.get("tax_type", "1"),
            "Amount": item["amount"],
            "SequenceNumber": item.get("sequence_number", "1"),
        }
        if item.get("unit"):
            pi["Unit"] = item["unit"]
        if item.get("remark"):
            pi["Remark"] = item["remark"]
        if item.get("related_number"):
            pi["RelateNumber"] = item["related_number"]
        product_items.append(pi)

    main = {
        "InvoiceNumber": invoice_number,
        "InvoiceDate": invoice_date,
        "InvoiceTime": invoice_time,
        "Seller": {"Identifier": seller_id},
        "Buyer": {"Identifier": buyer_id, "Name": buyer_name},
        "InvoiceType": invoice_type,
        "DonateMark": donate_mark,
        "PrintMark": print_mark,
        "RandomNumber": random_number,
    }
    if carrier_type:
        main["CarrierType"] = carrier_type
    if carrier_id1:
        main["CarrierID1"] = carrier_id1
    if carrier_id2:
        main["CarrierID2"] = carrier_id2
    if npo_ban:
        main["NPOBan"] = npo_ban
    if zero_tax_rate_reason:
        main["ZeroTaxRateReason"] = zero_tax_rate_reason
    if main_remark:
        main["MainRemark"] = main_remark

    payload = {
        "INVOICE_CODE": "C0401N",
        "Main": main,
        "Details": {"ProductItem": product_items},
        "Amount": {
            "SalesAmount": sales_amount,
            "FreeTaxSalesAmount": free_tax_sales_amount,
            "ZeroTaxSalesAmount": zero_tax_sales_amount,
            "TaxType": tax_type,
            "TaxRate": tax_rate,
            "TaxAmount": tax_amount,
            "TotalAmount": total_amount,
        },
    }

    return post_einvoice("C0401N", payload, wrapper="Invoice")


@mcp.tool()
def void_b2c_invoice(
    invoice_number: str = Field(description="Invoice number to void (10 chars)"),
    invoice_date: str = Field(description="Invoice date (yyyy-mm-dd)"),
    buyer_id: str = Field(description="Buyer tax ID"),
    seller_id: str = Field(description="Seller tax ID"),
    cancel_date: str = Field(description="Cancel date (yyyy-mm-dd)"),
    cancel_time: str = Field(description="Cancel time (HH:mm:ss)"),
    cancel_reason: str = Field(description="Reason for voiding the invoice"),
    return_tax_doc_number: Optional[str] = Field(default=None, description="Return tax document number"),
    remark: Optional[str] = Field(default=None, description="Additional remark"),
) -> dict:
    """Void a B2C invoice (C0501)."""
    payload = {
        "INVOICE_CODE": "C0501",
        "INVOICE_NUMBER": invoice_number,
        "INVOICE_DATE": invoice_date,
        "BUYERID": buyer_id,
        "SELLERID": seller_id,
        "CANCEL_DATE": cancel_date,
        "CANCEL_TIME": cancel_time,
        "CANCEL_REASON": cancel_reason,
        "RETURNTAXDOCUMENT_NUMBER": return_tax_doc_number or "",
        "REMARK": remark or "",
    }
    return post_einvoice("C0501", payload, wrapper="Invoice")
```

- [ ] **Step 4: Run tests**

Run: `python -m pytest tests/test_b2c_invoice_tools.py -v`
Expected: ALL PASSED

- [ ] **Step 5: Commit**

```bash
git add tools/b2c_invoice_tools.py tests/test_b2c_invoice_tools.py
git commit -m "feat: add B2C invoice tools (C0401, C0401N, C0501)"
```

---

### Task 7: B2B invoice tools (A0401, A0501, A0101, A0201)

**Files:**
- Create: `tools/b2b_invoice_tools.py`
- Create: `tests/test_b2b_invoice_tools.py`

- [ ] **Step 1: Write failing tests**

`tests/test_b2b_invoice_tools.py` — test that each tool sends the correct `INVOICE_CODE` and wrapper, and passes through the business fields. Follow the same pattern as Task 6 tests. Test:
- `create_b2b_invoice` sends `INVOICE_CODE: "A0401"` with nested Main/Details/Amount structure
- `void_b2b_invoice` sends `INVOICE_CODE: "A0501"` with CancelInvoiceNumber, InvoiceDate, CancelDate, CancelReason
- `create_b2b_exchange_invoice` sends `INVOICE_CODE: "A0101"` with nested structure (Seller.Address is mandatory)
- `void_b2b_exchange_invoice` sends `INVOICE_CODE: "A0201"` with CancelInvoiceNumber, CancelDate, CancelTime, CancelReason

- [ ] **Step 2: Run test to verify it fails**
- [ ] **Step 3: Implement `tools/b2b_invoice_tools.py`**

Implement 4 tools following the PDF spec structure:
- `create_b2b_invoice`: A0401 — Invoice wrapper, nested `Main` (InvoiceNumber, InvoiceDate, InvoiceTime, Seller{Identifier,Name,...}, Buyer{Identifier,Name,...}, InvoiceType, DonateMark, PrintMark), `Details` (ProductItem array), `Amount` (SalesAmount, TaxType, TaxRate, TaxAmount, TotalAmount)
- `void_b2b_invoice`: A0501 — Invoice wrapper, flat fields (CancelInvoiceNumber, InvoiceDate, BuyerId, SellerId, CancelDate, CancelTime, CancelReason, B_EMAIL_ADDRESS)
- `create_b2b_exchange_invoice`: A0101 — Invoice wrapper, same nested structure as A0401 but Seller.Address is mandatory, uses DTaxType for item tax type
- `void_b2b_exchange_invoice`: A0201 — Invoice wrapper, flat fields similar to A0501

- [ ] **Step 4: Run tests**
- [ ] **Step 5: Commit**

```bash
git add tools/b2b_invoice_tools.py tests/test_b2b_invoice_tools.py
git commit -m "feat: add B2B invoice tools (A0401, A0501, A0101, A0201)"
```

---

### Task 8: Allowance tools (D0401, D0401N, D0501, B0401, B0501, B0101)

**Files:**
- Create: `tools/allowance_tools.py`
- Create: `tests/test_allowance_tools.py`

- [ ] **Step 1: Write failing tests**

Test each tool sends correct wrapper and code:
- `create_b2c_allowance` (D0401): Invoice wrapper, `DISCOUNT_CODE: "D0401"`, flat fields (A1, A2, B1-B2, C1, D1-D11 for items)
- `create_b2c_allowance_n` (D0401N): Invoice wrapper, `INVOICE_CODE: "D0401N"`, flat fields with PRODUCTITEM array
- `void_b2c_allowance` (D0501): Invoice wrapper, `INVOICE_CODE: "D0501"`, flat fields
- `create_b2b_allowance` (B0401): Invoice wrapper, `INVOICE_CODE: "B0401"`, flat fields with PRODUCTITEM array
- `void_b2b_allowance` (B0501): **Allowance** wrapper, `INVOICE_CODE: "B0501"`
- `create_b2b_exchange_allowance` (B0101): Invoice wrapper, `INVOICE_CODE: "B0101"`, nested Main/Details/Amount

- [ ] **Step 2: Run test to verify it fails**
- [ ] **Step 3: Implement `tools/allowance_tools.py`**

Key implementation notes from PDF:
- D0401 uses DISCOUNT_CODE field (not INVOICE_CODE) at top level
- D0401N uses INVOICE_CODE
- B0501 is the ONLY function using the Allowance wrapper
- B0401 has ALLOWANCETYPE field (MIG4.1: "2" for seller's allowance notice)
- B0101 uses nested structure similar to A0401 but for allowances

- [ ] **Step 4: Run tests**
- [ ] **Step 5: Commit**

```bash
git add tools/allowance_tools.py tests/test_allowance_tools.py
git commit -m "feat: add allowance tools (D0401, D0401N, D0501, B0401, B0501, B0101)"
```

---

### Task 9: Cancel tools (C0701, B0701)

**Files:**
- Create: `tools/cancel_tools.py`
- Create: `tests/test_cancel_tools.py`

- [ ] **Step 1: Write failing tests**

- `cancel_invoice` (C0701): Invoice wrapper, `INVOICE_CODE: "C0701"`, fields: INVOICE_NUMBER, INVOICE_DATE, BUYERID, SELLERID, CANCEL_DATE, CANCEL_TIME, CANCEL_REASON
- `batch_cancel_invoice` (B0701): Invoice wrapper, `INVOICE_CODE: "B0701"`, includes full invoice data (buyer info, line items, amounts, etc.) with CANCEL_DATE, CANCEL_TIME, CANCEL_REASON at top level

- [ ] **Step 2: Run test to verify it fails**
- [ ] **Step 3: Implement `tools/cancel_tools.py`**
- [ ] **Step 4: Run tests**
- [ ] **Step 5: Commit**

```bash
git add tools/cancel_tools.py tests/test_cancel_tools.py
git commit -m "feat: add cancel tools (C0701, B0701)"
```

---

### Task 10: Query tools (Z11, Z31, Z33, Z34)

**Files:**
- Create: `tools/query_tools.py`
- Create: `tests/test_query_tools.py`

- [ ] **Step 1: Write failing tests**

- `get_cancel_status` (Z11): INDEX wrapper, `FUNCTIONCODE: "Z11"`, fields: INVOICE_NUMBER, INVOICE_DATE. Response includes STATUSCODE (1=completed, 2=pending, 3=failed)
- `get_downloaded_track_ranges` (Z31): Invoice wrapper, `INVOICE_CODE: "Z31"`, nested Main (HeadBan, BranchBan, InvoiceType, YearMonth, InvoiceTrack)
- `get_assignment_info` (Z33): Invoice wrapper, `INVOICE_CODE: "Z33"`, nested Main (HeadBan, BranchBan, YearMonth, InvoiceType)
- `download_winning_list` (Z34): Invoice wrapper, `INVOICE_CODE: "Z34"`, fields: YearMonth. Note: response may contain FILE_CONTENT binary data

- [ ] **Step 2: Run test to verify it fails**
- [ ] **Step 3: Implement `tools/query_tools.py`**
- [ ] **Step 4: Run tests**
- [ ] **Step 5: Commit**

```bash
git add tools/query_tools.py tests/test_query_tools.py
git commit -m "feat: add query tools (Z11, Z31, Z33, Z34)"
```

---

### Task 11: Admin tools (Z32, E0401, E0402)

**Files:**
- Create: `tools/admin_tools.py`
- Create: `tests/test_admin_tools.py`

- [ ] **Step 1: Write failing tests**

- `upload_next_period_tracks` (Z32): Invoice wrapper, `INVOICE_CODE: "Z32"`, fields for track upload
- `get_branch_assignment` (E0401): Invoice wrapper, `INVOICE_CODE: "E0401"`, nested Main (HeadBan, BranchBan, InvoiceType, YearMonth, InvoiceTrack, InvoiceBeginNo, InvoiceEndNo) + Details (BranchTrackItem array)
- `get_unused_tracks` (E0402): Invoice wrapper, `INVOICE_CODE: "E0402"`, nested Main (HeadBan, BranchBan, InvoiceType, YearMonth, InvoiceTrack) + Details (BranchTrackBlankItem array)

- [ ] **Step 2: Run test to verify it fails**
- [ ] **Step 3: Implement `tools/admin_tools.py`**
- [ ] **Step 4: Run tests**
- [ ] **Step 5: Commit**

```bash
git add tools/admin_tools.py tests/test_admin_tools.py
git commit -m "feat: add admin tools (Z32, E0401, E0402)"
```

---

### Task 12: Entry point and wiring

**Files:**
- Modify: `mcp_server.py`
- Modify: `.mcp.json`

- [ ] **Step 1: Update `mcp_server.py`**

```python
#!/usr/bin/env python3
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import tool modules to trigger @mcp.tool() decorator registration.
import tools.system_tools  # noqa: F401
import tools.invoice_number_tools  # noqa: F401
import tools.b2c_invoice_tools  # noqa: F401
import tools.b2b_invoice_tools  # noqa: F401
import tools.allowance_tools  # noqa: F401
import tools.cancel_tools  # noqa: F401
import tools.query_tools  # noqa: F401
import tools.admin_tools  # noqa: F401

from app import mcp


def main():
    mcp.run()


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run all unit tests**

Run: `python -m pytest tests/ -v --ignore=tests/test_regression.py`
Expected: ALL PASSED

- [ ] **Step 3: Commit**

```bash
git add mcp_server.py
git commit -m "feat: wire all 8 tool modules into mcp_server.py"
```

---

### Task 13: Regression tests (live API)

**Files:**
- Create: `tests/test_regression.py`

These tests hit the real test environment. Run with: `python -m pytest tests/test_regression.py -v -s`

- [ ] **Step 1: Create regression test file**

`tests/test_regression.py`:
```python
"""Regression tests against the live Universal EC test environment.

Run with: python -m pytest tests/test_regression.py -v -s
Requires .env with valid test credentials.
"""

import os
import pytest
from dotenv import load_dotenv

load_dotenv()

# Skip all tests if no real credentials
pytestmark = pytest.mark.skipif(
    not os.environ.get("EINVOICE_SELLER_ID") or os.environ.get("EINVOICE_SELLER_ID") == "your_seller_id",
    reason="No real credentials configured — skipping regression tests",
)


@pytest.fixture(autouse=True)
def use_real_env(monkeypatch):
    """Override the mock_env fixture — use real .env values."""
    load_dotenv(override=True)


class TestY01Connection:
    def test_connection_succeeds(self):
        from tools.system_tools import get_system_time
        result = get_system_time()
        assert result["INDEX"]["REPLY"] == "1"
        assert result["INDEX"]["MESSAGE"] == "連線成功"
        assert result["INDEX"]["SYSTIME"]  # should have a timestamp


class TestA01InvoiceNumbers:
    def test_get_current_period_numbers(self):
        from tools.invoice_number_tools import get_invoice_numbers
        result = get_invoice_numbers()
        idx = result["INDEX"]
        assert idx["FUNCTIONCODE"] == "A01"
        # REPLY 1 = success, 0 = failure (may fail if no numbers allocated)
        if idx["REPLY"] == "1":
            assert idx["INVOICEHEADER"]  # 2-letter track
            assert idx["INVOICESTART"]
            assert idx["INVOICEEND"]
            assert idx["QRCodeASKey"]


class TestC01NextPeriod:
    def test_get_next_period_numbers(self):
        from tools.invoice_number_tools import get_next_period_numbers
        result = get_next_period_numbers()
        assert result["INDEX"]["FUNCTIONCODE"] == "C01"


class TestZ21Expanded:
    def test_get_expanded_numbers(self):
        from tools.invoice_number_tools import get_invoice_numbers_expanded
        result = get_invoice_numbers_expanded()
        idx = result["INDEX"]
        assert idx["FUNCTIONCODE"] == "Z21"
        if idx["REPLY"] == "1" and "INVOICEDATA" in idx:
            for inv in idx["INVOICEDATA"]:
                assert "INVOICE_NUMBER" in inv
                assert "AESKEY" in inv
                assert "RANDOMNUMBER" in inv


class TestZ22NextPeriodExpanded:
    def test_get_next_period_expanded(self):
        from tools.invoice_number_tools import get_next_period_numbers_expanded
        result = get_next_period_numbers_expanded()
        assert result["INDEX"]["FUNCTIONCODE"] == "Z22"
```

- [ ] **Step 2: Run regression tests**

Run: `python -m pytest tests/test_regression.py -v -s`
Expected: Y01 PASSED (connection test), A01/C01/Z21/Z22 should pass or skip gracefully

- [ ] **Step 3: Run full test suite**

Run: `python -m pytest tests/ -v`
Expected: ALL PASSED (unit tests with mocks + regression tests with real API)

- [ ] **Step 4: Commit**

```bash
git add tests/test_regression.py
git commit -m "test: add regression tests against live test environment"
```

---

### Task 14: Final verification and CLAUDE.md update

- [ ] **Step 1: Update CLAUDE.md**

Update the CLAUDE.md to reflect the actual project (not the template).

- [ ] **Step 2: Run full test suite one final time**

```bash
python -m pytest tests/ -v
```

- [ ] **Step 3: Test MCP server starts**

```bash
echo '{"jsonrpc":"2.0","method":"initialize","params":{"capabilities":{}},"id":1}' | python mcp_server.py
```
Should not crash.

- [ ] **Step 4: Final commit**

```bash
git add -A
git commit -m "docs: update CLAUDE.md and finalize project setup"
```
