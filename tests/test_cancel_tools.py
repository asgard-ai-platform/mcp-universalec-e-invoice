import json


SAMPLE_ITEM = {
    "B1": "1", "B2": "Widget", "B3": "2", "B5": "100",
    "B6": "200", "B7": "1", "B13": "10",
}


class TestCancelInvoice:
    def test_c0701_payload_structure(self, mocker, mock_env):
        mock_resp = mocker.Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"Invoice": {"REPLY": "1"}}
        mock_post = mocker.patch("connectors.einvoice_client.requests.post", return_value=mock_resp)

        from tools.cancel_tools import cancel_invoice
        result = cancel_invoice(
            invoice_number="AB12345678",
            invoice_date="20240101",
            buyer_id="",
            seller_id="12345678",
            cancel_date="20240115",
            cancel_time="100000",
            cancel_reason="Customer request",
        )
        called_body = json.loads(mock_post.call_args[1]["data"])
        inv = called_body["Invoice"]
        assert inv["INVOICE_CODE"] == "C0701"
        assert inv["INVOICE_NUMBER"] == "AB12345678"
        assert inv["INVOICE_DATE"] == "20240101"
        assert inv["SELLERID"] == "12345678"
        assert inv["CANCEL_DATE"] == "20240115"
        assert inv["CANCEL_REASON"] == "Customer request"
        assert result["Invoice"]["REPLY"] == "1"

    def test_c0701_uses_invoice_wrapper(self, mocker, mock_env):
        mock_resp = mocker.Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"Invoice": {"REPLY": "1"}}
        mock_post = mocker.patch("connectors.einvoice_client.requests.post", return_value=mock_resp)

        from tools.cancel_tools import cancel_invoice
        cancel_invoice(
            invoice_number="AB12345678",
            invoice_date="20240101",
            buyer_id="",
            seller_id="12345678",
            cancel_date="20240115",
            cancel_time="100000",
            cancel_reason="Error",
        )
        called_body = json.loads(mock_post.call_args[1]["data"])
        assert "Invoice" in called_body
        assert "INDEX" not in called_body


class TestBatchCancelInvoice:
    def test_b0701_payload_structure(self, mocker, mock_env):
        mock_resp = mocker.Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"Invoice": {"REPLY": "1"}}
        mock_post = mocker.patch("connectors.einvoice_client.requests.post", return_value=mock_resp)

        from tools.cancel_tools import batch_cancel_invoice
        result = batch_cancel_invoice(
            cancel_date="20240115",
            cancel_time="100000",
            cancel_reason="Error",
            invoice_number="AB12345678",
            invoice_date="20240101",
            invoice_time="120000",
            buyer_id="",
            buyer_name="Buyer",
            invoice_type="07",
            donate_mark="0",
            print_mark="Y",
            random_number="1234",
            items=[SAMPLE_ITEM],
            sales_amount="200",
            free_tax="0",
            zero_tax="0",
            tax_type="1",
            tax_rate="0.05",
            tax_amount="10",
            total="210",
        )
        called_body = json.loads(mock_post.call_args[1]["data"])
        inv = called_body["Invoice"]
        assert inv["INVOICE_CODE"] == "B0701"
        assert inv["CANCEL_DATE"] == "20240115"
        assert inv["CANCEL_REASON"] == "Error"
        assert inv["A2"] == "AB12345678"
        assert inv["A3"] == "20240101"
        assert inv["B"] == [SAMPLE_ITEM]
        assert inv["C1"] == "200"
        assert inv["C7"] == "210"
        assert result["Invoice"]["REPLY"] == "1"

    def test_b0701_uses_invoice_wrapper(self, mocker, mock_env):
        mock_resp = mocker.Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"Invoice": {"REPLY": "1"}}
        mock_post = mocker.patch("connectors.einvoice_client.requests.post", return_value=mock_resp)

        from tools.cancel_tools import batch_cancel_invoice
        batch_cancel_invoice(
            cancel_date="20240115",
            cancel_time="100000",
            cancel_reason="Error",
            invoice_number="AB12345678",
            invoice_date="20240101",
            invoice_time="120000",
            buyer_id="",
            buyer_name="Buyer",
            invoice_type="07",
            donate_mark="0",
            print_mark="Y",
            random_number="0000",
            items=[SAMPLE_ITEM],
            sales_amount="200",
            free_tax="0",
            zero_tax="0",
            tax_type="1",
            tax_rate="0.05",
            tax_amount="10",
            total="210",
        )
        called_body = json.loads(mock_post.call_args[1]["data"])
        assert "Invoice" in called_body
        assert "INDEX" not in called_body
