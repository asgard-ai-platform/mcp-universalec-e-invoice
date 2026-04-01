"""Regression tests against the live Universal EC test environment.

Run with: pytest tests/test_regression.py -v -s
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
    """Override the mock_env autouse fixture — use real .env values."""
    load_dotenv(override=True)
    # Re-set from actual .env so mock_env doesn't override
    for key in ["EINVOICE_BASE_URL", "EINVOICE_SELLER_ID", "EINVOICE_POS_ID", "EINVOICE_POS_SN"]:
        val = os.environ.get(key)
        if val:
            monkeypatch.setenv(key, val)


class TestY01Connection:
    def test_connection_succeeds(self):
        from tools.system_tools import get_system_time
        result = get_system_time()
        assert result["INDEX"]["REPLY"] == "1"
        assert result["INDEX"]["MESSAGE"] == "連線成功"
        assert result["INDEX"]["SYSTIME"]


class TestA01InvoiceNumbers:
    def test_get_current_period_numbers(self):
        from tools.invoice_number_tools import get_invoice_numbers
        result = get_invoice_numbers()
        idx = result["INDEX"]
        assert idx["FUNCTIONCODE"] == "A01"
        if idx["REPLY"] == "1":
            assert idx["INVOICEHEADER"]
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
