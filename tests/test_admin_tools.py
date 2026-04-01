import json


class TestUploadNextPeriodTracks:
    def test_z32_payload_structure(self, mocker, mock_env):
        mock_resp = mocker.Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"Invoice": {"REPLY": "1"}}
        mock_post = mocker.patch("connectors.einvoice_client.requests.post", return_value=mock_resp)

        from tools.admin_tools import upload_next_period_tracks
        result = upload_next_period_tracks(
            head_ban="12345678",
            branch_ban="12345678",
            invoice_type="07",
            year_month="11306",
            invoice_track="DC",
            invoice_begin_no="00000001",
            invoice_end_no="00000050",
        )
        called_body = json.loads(mock_post.call_args[1]["data"])
        inv = called_body["Invoice"]
        assert inv["INVOICE_CODE"] == "Z32"
        assert inv["HeadBan"] == "12345678"
        assert inv["InvoiceTrack"] == "DC"
        assert inv["InvoiceBeginNo"] == "00000001"
        assert inv["InvoiceEndNo"] == "00000050"
        assert inv["YearMonth"] == "11306"
        assert result["Invoice"]["REPLY"] == "1"

    def test_z32_uses_invoice_wrapper(self, mocker, mock_env):
        mock_resp = mocker.Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"Invoice": {"REPLY": "1"}}
        mock_post = mocker.patch("connectors.einvoice_client.requests.post", return_value=mock_resp)

        from tools.admin_tools import upload_next_period_tracks
        upload_next_period_tracks(
            head_ban="12345678",
            branch_ban="12345678",
            invoice_type="07",
            year_month="11306",
            invoice_track="DC",
            invoice_begin_no="00000001",
            invoice_end_no="00000050",
        )
        called_body = json.loads(mock_post.call_args[1]["data"])
        assert "Invoice" in called_body
        assert "INDEX" not in called_body


class TestAssignBranchTracks:
    def test_e0401_payload_structure(self, mocker, mock_env):
        mock_resp = mocker.Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"Invoice": {"REPLY": "1"}}
        mock_post = mocker.patch("connectors.einvoice_client.requests.post", return_value=mock_resp)

        branch_items = [{"InvoiceBeginNo": "00000001", "InvoiceEndNo": "00000025", "InvoiceBooklet": "1"}]

        from tools.admin_tools import assign_branch_tracks
        result = assign_branch_tracks(
            head_ban="12345678",
            branch_ban="99887766",
            invoice_type="07",
            year_month="11304",
            invoice_track="DC",
            invoice_begin_no="00000001",
            invoice_end_no="00000050",
            branch_track_items=branch_items,
        )
        called_body = json.loads(mock_post.call_args[1]["data"])
        inv = called_body["Invoice"]
        assert inv["INVOICE_CODE"] == "E0401"
        assert inv["Main"]["HeadBan"] == "12345678"
        assert inv["Main"]["BranchBan"] == "99887766"
        assert inv["Main"]["InvoiceTrack"] == "DC"
        assert inv["Details"]["BranchTrackItem"] == branch_items
        assert result["Invoice"]["REPLY"] == "1"

    def test_e0401_uses_invoice_wrapper(self, mocker, mock_env):
        mock_resp = mocker.Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"Invoice": {"REPLY": "1"}}
        mock_post = mocker.patch("connectors.einvoice_client.requests.post", return_value=mock_resp)

        from tools.admin_tools import assign_branch_tracks
        assign_branch_tracks(
            head_ban="12345678",
            branch_ban="99887766",
            invoice_type="07",
            year_month="11304",
            invoice_track="DC",
            invoice_begin_no="00000001",
            invoice_end_no="00000050",
            branch_track_items=[{"InvoiceBeginNo": "00000001", "InvoiceEndNo": "00000025", "InvoiceBooklet": "1"}],
        )
        called_body = json.loads(mock_post.call_args[1]["data"])
        assert "Invoice" in called_body
        assert "INDEX" not in called_body


class TestReportUnusedTracks:
    def test_e0402_payload_structure(self, mocker, mock_env):
        mock_resp = mocker.Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"Invoice": {"REPLY": "1"}}
        mock_post = mocker.patch("connectors.einvoice_client.requests.post", return_value=mock_resp)

        blank_items = [{"InvoiceBeginNo": "00000026", "InvoiceEndNo": "00000050"}]

        from tools.admin_tools import report_unused_tracks
        result = report_unused_tracks(
            head_ban="12345678",
            branch_ban="12345678",
            invoice_type="07",
            year_month="11304",
            invoice_track="DC",
            blank_items=blank_items,
        )
        called_body = json.loads(mock_post.call_args[1]["data"])
        inv = called_body["Invoice"]
        assert inv["INVOICE_CODE"] == "E0402"
        assert inv["Main"]["HeadBan"] == "12345678"
        assert inv["Main"]["InvoiceTrack"] == "DC"
        assert inv["Details"]["BranchTrackBlankItem"] == blank_items
        assert result["Invoice"]["REPLY"] == "1"

    def test_e0402_uses_invoice_wrapper(self, mocker, mock_env):
        mock_resp = mocker.Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"Invoice": {"REPLY": "1"}}
        mock_post = mocker.patch("connectors.einvoice_client.requests.post", return_value=mock_resp)

        from tools.admin_tools import report_unused_tracks
        report_unused_tracks(
            head_ban="12345678",
            branch_ban="12345678",
            invoice_type="07",
            year_month="11304",
            invoice_track="DC",
            blank_items=[{"InvoiceBeginNo": "00000026", "InvoiceEndNo": "00000050"}],
        )
        called_body = json.loads(mock_post.call_args[1]["data"])
        assert "Invoice" in called_body
        assert "INDEX" not in called_body
