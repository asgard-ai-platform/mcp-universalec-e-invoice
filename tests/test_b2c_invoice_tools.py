import json


SAMPLE_ITEM_POSITIONAL = {
    "B1": "1", "B2": "Widget", "B3": "2", "B5": "100",
    "B6": "200", "B7": "1", "B13": "10",
}

SAMPLE_ITEM_NAMED = {
    "Description": "Widget", "Quantity": "2", "UnitPrice": "100",
    "TaxType": "1", "Amount": "200", "SequenceNumber": "1",
}


class TestCreateB2cInvoice:
    def test_c0401_payload_structure(self, mocker, mock_env):
        mock_resp = mocker.Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"Invoice": {"INVOICE_CODE": "C0401", "REPLY": "1"}}
        mock_post = mocker.patch("connectors.einvoice_client.requests.post", return_value=mock_resp)

        from tools.b2c_invoice_tools import create_b2c_invoice
        result = create_b2c_invoice(
            invoice_number="AB12345678",
            invoice_date="20240101",
            invoice_time="120000",
            buyer_id="",
            buyer_name="Test Buyer",
            invoice_type="07",
            donate_mark="0",
            print_mark="Y",
            random_number="1234",
            items=[SAMPLE_ITEM_POSITIONAL],
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
        assert inv["A1"] == "C0401"
        assert inv["A2"] == "AB12345678"
        assert inv["A3"] == "20240101"
        assert inv["B"] == [SAMPLE_ITEM_POSITIONAL]
        assert inv["C1"] == "200"
        assert inv["C7"] == "210"
        assert result["Invoice"]["REPLY"] == "1"

    def test_c0401_uses_invoice_wrapper(self, mocker, mock_env):
        mock_resp = mocker.Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"Invoice": {"REPLY": "1"}}
        mock_post = mocker.patch("connectors.einvoice_client.requests.post", return_value=mock_resp)

        from tools.b2c_invoice_tools import create_b2c_invoice
        create_b2c_invoice(
            invoice_number="AB12345678",
            invoice_date="20240101",
            invoice_time="120000",
            buyer_id="",
            buyer_name="Buyer",
            invoice_type="07",
            donate_mark="0",
            print_mark="Y",
            random_number="0000",
            items=[SAMPLE_ITEM_POSITIONAL],
            sales_amount="100",
            free_tax="0",
            zero_tax="0",
            tax_type="1",
            tax_rate="0.05",
            tax_amount="5",
            total="105",
        )
        called_body = json.loads(mock_post.call_args[1]["data"])
        assert "Invoice" in called_body
        assert "INDEX" not in called_body


class TestCreateB2cInvoiceNamed:
    def test_c0401n_payload_structure(self, mocker, mock_env):
        mock_resp = mocker.Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"Invoice": {"REPLY": "1"}}
        mock_post = mocker.patch("connectors.einvoice_client.requests.post", return_value=mock_resp)

        from tools.b2c_invoice_tools import create_b2c_invoice_named
        result = create_b2c_invoice_named(
            invoice_number="AB12345678",
            invoice_date="20240101",
            invoice_time="120000",
            seller_identifier="12345678",
            buyer_identifier="",
            buyer_name="Test Buyer",
            invoice_type="07",
            donate_mark="0",
            print_mark="Y",
            random_number="1234",
            items=[SAMPLE_ITEM_NAMED],
            sales_amount="200",
            free_tax_sales_amount="0",
            zero_tax_sales_amount="0",
            amount_tax_type="1",
            tax_rate="0.05",
            tax_amount="10",
            total_amount="210",
        )
        called_body = json.loads(mock_post.call_args[1]["data"])
        inv = called_body["Invoice"]
        assert inv["INVOICE_CODE"] == "C0401N"
        assert inv["Main"]["InvoiceNumber"] == "AB12345678"
        assert inv["Main"]["Seller"]["Identifier"] == "12345678"
        assert inv["Main"]["Buyer"]["Name"] == "Test Buyer"
        assert inv["Details"]["ProductItem"] == [SAMPLE_ITEM_NAMED]
        assert inv["Amount"]["TotalAmount"] == "210"
        assert result["Invoice"]["REPLY"] == "1"

    def test_c0401n_uses_invoice_wrapper(self, mocker, mock_env):
        mock_resp = mocker.Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"Invoice": {"REPLY": "1"}}
        mock_post = mocker.patch("connectors.einvoice_client.requests.post", return_value=mock_resp)

        from tools.b2c_invoice_tools import create_b2c_invoice_named
        create_b2c_invoice_named(
            invoice_number="AB12345678",
            invoice_date="20240101",
            invoice_time="120000",
            seller_identifier="12345678",
            buyer_identifier="",
            buyer_name="Buyer",
            invoice_type="07",
            donate_mark="0",
            print_mark="Y",
            random_number="0000",
            items=[SAMPLE_ITEM_NAMED],
            sales_amount="100",
            free_tax_sales_amount="0",
            zero_tax_sales_amount="0",
            amount_tax_type="1",
            tax_rate="0.05",
            tax_amount="5",
            total_amount="105",
        )
        called_body = json.loads(mock_post.call_args[1]["data"])
        assert "Invoice" in called_body
        assert "INDEX" not in called_body


class TestVoidB2cInvoice:
    def test_c0501_payload_structure(self, mocker, mock_env):
        mock_resp = mocker.Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"Invoice": {"REPLY": "1"}}
        mock_post = mocker.patch("connectors.einvoice_client.requests.post", return_value=mock_resp)

        from tools.b2c_invoice_tools import void_b2c_invoice
        result = void_b2c_invoice(
            invoice_number="AB12345678",
            invoice_date="20240101",
            buyer_id="",
            seller_id="12345678",
            cancel_date="20240110",
            cancel_time="100000",
            cancel_reason="Customer request",
        )
        called_body = json.loads(mock_post.call_args[1]["data"])
        inv = called_body["Invoice"]
        assert inv["INVOICE_CODE"] == "C0501"
        assert inv["INVOICE_NUMBER"] == "AB12345678"
        assert inv["INVOICE_DATE"] == "20240101"
        assert inv["CANCEL_DATE"] == "20240110"
        assert inv["CANCEL_REASON"] == "Customer request"
        assert result["Invoice"]["REPLY"] == "1"

    def test_c0501_uses_invoice_wrapper(self, mocker, mock_env):
        mock_resp = mocker.Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"Invoice": {"REPLY": "1"}}
        mock_post = mocker.patch("connectors.einvoice_client.requests.post", return_value=mock_resp)

        from tools.b2c_invoice_tools import void_b2c_invoice
        void_b2c_invoice(
            invoice_number="AB12345678",
            invoice_date="20240101",
            buyer_id="",
            seller_id="12345678",
            cancel_date="20240110",
            cancel_time="100000",
            cancel_reason="Error",
        )
        called_body = json.loads(mock_post.call_args[1]["data"])
        assert "Invoice" in called_body
        assert "INDEX" not in called_body
