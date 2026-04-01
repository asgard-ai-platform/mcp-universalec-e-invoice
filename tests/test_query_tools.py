import json


class TestGetCancelStatus:
    def test_z11_payload_structure(self, mocker, mock_env):
        mock_resp = mocker.Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"INDEX": {"FUNCTIONCODE": "Z11", "STATUSCODE": "1", "REPLY": "1"}}
        mock_post = mocker.patch("connectors.einvoice_client.requests.post", return_value=mock_resp)

        from tools.query_tools import get_cancel_status
        result = get_cancel_status(
            invoice_number="AB12345678",
            invoice_date="20240101",
        )
        called_body = json.loads(mock_post.call_args[1]["data"])
        idx = called_body["INDEX"]
        assert idx["FUNCTIONCODE"] == "Z11"
        assert idx["INVOICE_NUMBER"] == "AB12345678"
        assert idx["INVOICE_DATE"] == "20240101"
        assert result["INDEX"]["STATUSCODE"] == "1"

    def test_z11_uses_index_wrapper(self, mocker, mock_env):
        mock_resp = mocker.Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"INDEX": {"REPLY": "1"}}
        mock_post = mocker.patch("connectors.einvoice_client.requests.post", return_value=mock_resp)

        from tools.query_tools import get_cancel_status
        get_cancel_status(invoice_number="AB12345678", invoice_date="20240101")
        called_body = json.loads(mock_post.call_args[1]["data"])
        assert "INDEX" in called_body
        assert "Invoice" not in called_body


class TestGetDownloadedTrackRanges:
    def test_z31_payload_structure(self, mocker, mock_env):
        mock_resp = mocker.Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"Invoice": {"REPLY": "1"}}
        mock_post = mocker.patch("connectors.einvoice_client.requests.post", return_value=mock_resp)

        from tools.query_tools import get_downloaded_track_ranges
        result = get_downloaded_track_ranges(
            head_ban="12345678",
            branch_ban="12345678",
            invoice_type="07",
            year_month="11304",
            invoice_track="DC",
        )
        called_body = json.loads(mock_post.call_args[1]["data"])
        inv = called_body["Invoice"]
        assert inv["INVOICE_CODE"] == "Z31"
        assert inv["Main"]["HeadBan"] == "12345678"
        assert inv["Main"]["InvoiceTrack"] == "DC"
        assert inv["Main"]["YearMonth"] == "11304"
        assert result["Invoice"]["REPLY"] == "1"

    def test_z31_uses_invoice_wrapper(self, mocker, mock_env):
        mock_resp = mocker.Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"Invoice": {"REPLY": "1"}}
        mock_post = mocker.patch("connectors.einvoice_client.requests.post", return_value=mock_resp)

        from tools.query_tools import get_downloaded_track_ranges
        get_downloaded_track_ranges(
            head_ban="12345678",
            branch_ban="12345678",
            invoice_type="07",
            year_month="11304",
            invoice_track="DC",
        )
        called_body = json.loads(mock_post.call_args[1]["data"])
        assert "Invoice" in called_body
        assert "INDEX" not in called_body


class TestGetAssignmentInfo:
    def test_z33_payload_structure(self, mocker, mock_env):
        mock_resp = mocker.Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"Invoice": {"REPLY": "1"}}
        mock_post = mocker.patch("connectors.einvoice_client.requests.post", return_value=mock_resp)

        from tools.query_tools import get_assignment_info
        result = get_assignment_info(
            head_ban="12345678",
            branch_ban="12345678",
            year_month="11304",
            invoice_type="07",
        )
        called_body = json.loads(mock_post.call_args[1]["data"])
        inv = called_body["Invoice"]
        assert inv["INVOICE_CODE"] == "Z33"
        assert inv["Main"]["HeadBan"] == "12345678"
        assert inv["Main"]["YearMonth"] == "11304"
        assert inv["Main"]["InvoiceType"] == "07"
        assert result["Invoice"]["REPLY"] == "1"


class TestGetWinningList:
    def test_z34_payload_structure(self, mocker, mock_env):
        mock_resp = mocker.Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"Invoice": {"REPLY": "1", "WinningNumbers": []}}
        mock_post = mocker.patch("connectors.einvoice_client.requests.post", return_value=mock_resp)

        from tools.query_tools import get_winning_list
        result = get_winning_list(year_month="11304")
        called_body = json.loads(mock_post.call_args[1]["data"])
        inv = called_body["Invoice"]
        assert inv["INVOICE_CODE"] == "Z34"
        assert inv["YearMonth"] == "11304"
        assert result["Invoice"]["REPLY"] == "1"

    def test_z34_uses_invoice_wrapper(self, mocker, mock_env):
        mock_resp = mocker.Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"Invoice": {"REPLY": "1"}}
        mock_post = mocker.patch("connectors.einvoice_client.requests.post", return_value=mock_resp)

        from tools.query_tools import get_winning_list
        get_winning_list(year_month="11304")
        called_body = json.loads(mock_post.call_args[1]["data"])
        assert "Invoice" in called_body
        assert "INDEX" not in called_body
