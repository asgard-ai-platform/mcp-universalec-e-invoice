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
