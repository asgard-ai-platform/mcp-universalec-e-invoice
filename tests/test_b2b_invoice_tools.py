import json


SAMPLE_ITEM = {
    "Description": "Widget", "Quantity": "2", "UnitPrice": "100",
    "TaxType": "1", "Amount": "200", "SequenceNumber": "1",
}

SAMPLE_EXCHANGE_ITEM = {
    "Description": "Widget", "Quantity": "2", "UnitPrice": "100",
    "DTaxType": "1", "Amount": "200", "SequenceNumber": "1",
}


class TestCreateB2bInvoice:
    def test_a0401_payload_structure(self, mocker, mock_env):
        mock_resp = mocker.Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"Invoice": {"REPLY": "1"}}
        mock_post = mocker.patch("connectors.einvoice_client.requests.post", return_value=mock_resp)

        from tools.b2b_invoice_tools import create_b2b_invoice
        result = create_b2b_invoice(
            invoice_number="AB12345678",
            invoice_date="20240101",
            invoice_time="120000",
            seller_identifier="12345678",
            seller_name="Seller Corp",
            buyer_identifier="87654321",
            buyer_name="Buyer Corp",
            invoice_type="07",
            donate_mark="0",
            print_mark="Y",
            items=[SAMPLE_ITEM],
            sales_amount="200",
            tax_type="1",
            tax_rate="0.05",
            tax_amount="10",
            total_amount="210",
        )
        called_body = json.loads(mock_post.call_args[1]["data"])
        inv = called_body["Invoice"]
        assert inv["INVOICE_CODE"] == "A0401"
        assert inv["Main"]["InvoiceNumber"] == "AB12345678"
        assert inv["Main"]["Seller"]["Identifier"] == "12345678"
        assert inv["Main"]["Seller"]["Name"] == "Seller Corp"
        assert inv["Main"]["Buyer"]["Identifier"] == "87654321"
        assert inv["Details"]["ProductItem"] == [SAMPLE_ITEM]
        assert inv["Amount"]["TotalAmount"] == "210"
        assert "Invoice" in called_body
        assert result["Invoice"]["REPLY"] == "1"

    def test_a0401_uses_invoice_wrapper(self, mocker, mock_env):
        mock_resp = mocker.Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"Invoice": {"REPLY": "1"}}
        mock_post = mocker.patch("connectors.einvoice_client.requests.post", return_value=mock_resp)

        from tools.b2b_invoice_tools import create_b2b_invoice
        create_b2b_invoice(
            invoice_number="AB12345678",
            invoice_date="20240101",
            invoice_time="120000",
            seller_identifier="12345678",
            seller_name="Seller",
            buyer_identifier="87654321",
            buyer_name="Buyer",
            invoice_type="07",
            donate_mark="0",
            print_mark="Y",
            items=[SAMPLE_ITEM],
            sales_amount="200",
            tax_type="1",
            tax_rate="0.05",
            tax_amount="10",
            total_amount="210",
        )
        called_body = json.loads(mock_post.call_args[1]["data"])
        assert "Invoice" in called_body
        assert "INDEX" not in called_body


class TestVoidB2bInvoice:
    def test_a0501_payload_structure(self, mocker, mock_env):
        mock_resp = mocker.Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"Invoice": {"REPLY": "1"}}
        mock_post = mocker.patch("connectors.einvoice_client.requests.post", return_value=mock_resp)

        from tools.b2b_invoice_tools import void_b2b_invoice
        result = void_b2b_invoice(
            cancel_invoice_number="AB12345678",
            invoice_date="20240101",
            buyer_id="87654321",
            seller_id="12345678",
            cancel_date="20240110",
            cancel_time="100000",
            cancel_reason="Customer request",
        )
        called_body = json.loads(mock_post.call_args[1]["data"])
        inv = called_body["Invoice"]
        assert inv["INVOICE_CODE"] == "A0501"
        assert inv["CancelInvoiceNumber"] == "AB12345678"
        assert inv["BuyerId"] == "87654321"
        assert inv["SellerId"] == "12345678"
        assert inv["CancelReason"] == "Customer request"
        assert result["Invoice"]["REPLY"] == "1"


class TestCreateB2bExchangeInvoice:
    def test_a0101_payload_structure(self, mocker, mock_env):
        mock_resp = mocker.Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"Invoice": {"REPLY": "1"}}
        mock_post = mocker.patch("connectors.einvoice_client.requests.post", return_value=mock_resp)

        from tools.b2b_invoice_tools import create_b2b_exchange_invoice
        result = create_b2b_exchange_invoice(
            invoice_number="AB12345678",
            invoice_date="20240101",
            invoice_time="120000",
            seller_identifier="12345678",
            seller_name="Seller Corp",
            seller_address="123 Main St",
            buyer_identifier="87654321",
            buyer_name="Buyer Corp",
            invoice_type="07",
            donate_mark="0",
            print_mark="Y",
            items=[SAMPLE_EXCHANGE_ITEM],
            sales_amount="200",
            tax_type="1",
            tax_rate="0.05",
            tax_amount="10",
            total_amount="210",
        )
        called_body = json.loads(mock_post.call_args[1]["data"])
        inv = called_body["Invoice"]
        assert inv["INVOICE_CODE"] == "A0101"
        assert inv["Main"]["Seller"]["Address"] == "123 Main St"
        assert inv["Details"]["ProductItem"] == [SAMPLE_EXCHANGE_ITEM]
        assert result["Invoice"]["REPLY"] == "1"

    def test_a0101_seller_address_in_payload(self, mocker, mock_env):
        mock_resp = mocker.Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"Invoice": {"REPLY": "1"}}
        mock_post = mocker.patch("connectors.einvoice_client.requests.post", return_value=mock_resp)

        from tools.b2b_invoice_tools import create_b2b_exchange_invoice
        create_b2b_exchange_invoice(
            invoice_number="AB12345678",
            invoice_date="20240101",
            invoice_time="120000",
            seller_identifier="12345678",
            seller_name="Seller",
            seller_address="456 Other Ave",
            buyer_identifier="87654321",
            buyer_name="Buyer",
            invoice_type="07",
            donate_mark="0",
            print_mark="Y",
            items=[SAMPLE_EXCHANGE_ITEM],
            sales_amount="200",
            tax_type="1",
            tax_rate="0.05",
            tax_amount="10",
            total_amount="210",
        )
        called_body = json.loads(mock_post.call_args[1]["data"])
        assert "Address" in called_body["Invoice"]["Main"]["Seller"]


class TestVoidB2bExchangeInvoice:
    def test_a0201_payload_structure(self, mocker, mock_env):
        mock_resp = mocker.Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"Invoice": {"REPLY": "1"}}
        mock_post = mocker.patch("connectors.einvoice_client.requests.post", return_value=mock_resp)

        from tools.b2b_invoice_tools import void_b2b_exchange_invoice
        result = void_b2b_exchange_invoice(
            cancel_invoice_number="AB12345678",
            invoice_date="20240101",
            buyer_id="87654321",
            seller_id="12345678",
            cancel_date="20240110",
            cancel_time="100000",
            cancel_reason="Error",
        )
        called_body = json.loads(mock_post.call_args[1]["data"])
        inv = called_body["Invoice"]
        assert inv["INVOICE_CODE"] == "A0201"
        assert inv["CancelInvoiceNumber"] == "AB12345678"
        assert inv["BuyerId"] == "87654321"
        assert result["Invoice"]["REPLY"] == "1"
