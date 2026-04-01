import os
import pytest


@pytest.fixture(autouse=True)
def mock_env(monkeypatch):
    monkeypatch.setenv("EINVOICE_BASE_URL", "https://test.example.com/GetInvoice.ashx")
    monkeypatch.setenv("EINVOICE_SELLER_ID", "12345678")
    monkeypatch.setenv("EINVOICE_POS_ID", "T001")
    monkeypatch.setenv("EINVOICE_POS_SN", "test_possn_key_123")


@pytest.fixture
def mock_post_success(mocker):
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
