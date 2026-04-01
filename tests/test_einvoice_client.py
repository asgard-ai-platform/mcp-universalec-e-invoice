import json

import pytest

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
    monkeypatch.delenv("EINVOICE_BASE_URL", raising=False)
    with pytest.raises(RuntimeError, match="EINVOICE_SELLER_ID"):
        get_credentials()


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

    def test_index_wrapper_preserves_custom_payload(self, mocker, mock_env):
        mock_resp = mocker.Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"INDEX": {"REPLY": "1"}}
        mock_post = mocker.patch("connectors.einvoice_client.requests.post", return_value=mock_resp)

        post_einvoice("A01", {"TAXMONTH": "11304", "INVOICEHEADER": "DC"})
        called_body = json.loads(mock_post.call_args[1]["data"])
        assert called_body["INDEX"]["TAXMONTH"] == "11304"
        assert called_body["INDEX"]["INVOICEHEADER"] == "DC"


class TestPostEinvoiceInvoiceWrapper:
    def test_invoice_wrapper_structure(self, mocker, mock_env):
        mock_resp = mocker.Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"INDEX": {"FUNCTIONCODE": "C0401", "REPLY": "1"}}
        mock_post = mocker.patch("connectors.einvoice_client.requests.post", return_value=mock_resp)

        post_einvoice("C0401", {"A1": "C0401", "A2": "AB12345678"}, wrapper="Invoice")
        called_body = json.loads(mock_post.call_args[1]["data"])
        assert "Invoice" in called_body
        assert called_body["Invoice"]["A1"] == "C0401"
        assert called_body["Invoice"]["POSSN"] == "test_possn_key_123"
        assert called_body["Invoice"]["POSID"] == "T001"


class TestPostEinvoiceAllowanceWrapper:
    def test_allowance_wrapper(self, mocker, mock_env):
        mock_resp = mocker.Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"INDEX": {"FUNCTIONCODE": "B0501", "REPLY": "1"}}
        mock_post = mocker.patch("connectors.einvoice_client.requests.post", return_value=mock_resp)

        post_einvoice("B0501", {"INVOICE_CODE": "B0501"}, wrapper="Allowance")
        called_body = json.loads(mock_post.call_args[1]["data"])
        assert "Allowance" in called_body
        assert called_body["Allowance"]["POSSN"] == "test_possn_key_123"


class TestPostEinvoiceErrorHandling:
    def test_http_error_raises(self, mocker, mock_env):
        mock_resp = mocker.Mock()
        mock_resp.status_code = 500
        mock_resp.text = "Internal Server Error"
        mocker.patch("connectors.einvoice_client.requests.post", return_value=mock_resp)

        with pytest.raises(EInvoiceAPIError, match="500"):
            post_einvoice("Y01", {})

    def test_connection_error_retries(self, mocker, mock_env):
        import requests as req
        mock_post = mocker.patch(
            "connectors.einvoice_client.requests.post",
            side_effect=req.exceptions.ConnectionError("refused"),
        )
        with pytest.raises(EInvoiceAPIError, match="retries"):
            post_einvoice("Y01", {}, retries=2)
        assert mock_post.call_count == 2
