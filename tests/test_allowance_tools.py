import json


SAMPLE_ITEM_POSITIONAL = {
    "D1": "1", "D2": "20240101", "D3": "AB12345678", "D4": "1",
    "D5": "Widget", "D6": "2", "D8": "100", "D9": "200", "D10": "10", "D11": "1",
}

SAMPLE_ITEM_NAMED = {
    "ORIGINALINVOICEDATE": "20240101",
    "ORIGINALINVOICENUMBER": "AB12345678",
    "ALLOWANCESEQUENCENUMBER": "1",
    "ORIGINALDESCRIPTION": "Widget",
    "QUANTITY": "2",
    "UNITPRICE": "100",
    "AMOUNT": "200",
    "TAX": "10",
    "TAXTYPE": "1",
}


class TestCreateB2cAllowance:
    def test_d0401_payload_structure(self, mocker, mock_env):
        mock_resp = mocker.Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"Invoice": {"REPLY": "1"}}
        mock_post = mocker.patch("connectors.einvoice_client.requests.post", return_value=mock_resp)

        from tools.allowance_tools import create_b2c_allowance
        result = create_b2c_allowance(
            allowance_number="ZZ00000001",
            allowance_date="20240115",
            buyer_id="",
            buyer_name="Test Buyer",
            allowance_type="2",
            items=[SAMPLE_ITEM_POSITIONAL],
            tax_amount="10",
            total_amount="210",
        )
        called_body = json.loads(mock_post.call_args[1]["data"])
        inv = called_body["Invoice"]
        assert inv["DISCOUNT_CODE"] == "D0401"
        assert inv["A1"] == "ZZ00000001"
        assert inv["A2"] == "20240115"
        assert inv["B1"] == ""
        assert inv["C1"] == "2"
        assert inv["C2"] == "10"
        assert inv["C3"] == "210"
        assert inv["D"] == [SAMPLE_ITEM_POSITIONAL]
        assert "Invoice" in called_body
        assert result["Invoice"]["REPLY"] == "1"

    def test_d0401_uses_invoice_wrapper(self, mocker, mock_env):
        mock_resp = mocker.Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"Invoice": {"REPLY": "1"}}
        mock_post = mocker.patch("connectors.einvoice_client.requests.post", return_value=mock_resp)

        from tools.allowance_tools import create_b2c_allowance
        create_b2c_allowance(
            allowance_number="ZZ00000001",
            allowance_date="20240115",
            buyer_id="",
            buyer_name="Buyer",
            allowance_type="2",
            items=[SAMPLE_ITEM_POSITIONAL],
            tax_amount="10",
            total_amount="210",
        )
        called_body = json.loads(mock_post.call_args[1]["data"])
        assert "Invoice" in called_body
        assert "Allowance" not in called_body


class TestCreateB2cAllowanceNamed:
    def test_d0401n_payload_structure(self, mocker, mock_env):
        mock_resp = mocker.Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"Invoice": {"REPLY": "1"}}
        mock_post = mocker.patch("connectors.einvoice_client.requests.post", return_value=mock_resp)

        from tools.allowance_tools import create_b2c_allowance_named
        result = create_b2c_allowance_named(
            allowance_number="ZZ00000001",
            allowance_date="20240115",
            buyer_identifier="",
            buyer_name="Test Buyer",
            allowance_type="2",
            items=[SAMPLE_ITEM_NAMED],
            tax_amount="10",
            total_amount="210",
        )
        called_body = json.loads(mock_post.call_args[1]["data"])
        inv = called_body["Invoice"]
        assert inv["INVOICE_CODE"] == "D0401N"
        assert inv["ALLOWANCENUMBER"] == "ZZ00000001"
        assert inv["IDENTIFIER"] == ""
        assert inv["PRODUCTITEM"] == [SAMPLE_ITEM_NAMED]
        assert inv["TAXAMOUNT"] == "10"
        assert inv["TOTALAMOUNT"] == "210"
        assert result["Invoice"]["REPLY"] == "1"


class TestVoidB2cAllowance:
    def test_d0501_payload_structure(self, mocker, mock_env):
        mock_resp = mocker.Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"Invoice": {"REPLY": "1"}}
        mock_post = mocker.patch("connectors.einvoice_client.requests.post", return_value=mock_resp)

        from tools.allowance_tools import void_b2c_allowance
        result = void_b2c_allowance(
            allowance_number="ZZ00000001",
            allowance_date="20240115",
            buyer_id="",
            seller_id="12345678",
            cancel_date="20240120",
            cancel_time="100000",
            cancel_reason="Error",
        )
        called_body = json.loads(mock_post.call_args[1]["data"])
        inv = called_body["Invoice"]
        assert inv["INVOICE_CODE"] == "D0501"
        assert inv["INVOICE_NUMBER"] == "ZZ00000001"
        assert inv["INVOICE_DATE"] == "20240115"
        assert inv["SELLERID"] == "12345678"
        assert result["Invoice"]["REPLY"] == "1"


class TestCreateB2bAllowance:
    def test_b0401_payload_structure(self, mocker, mock_env):
        mock_resp = mocker.Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"Invoice": {"REPLY": "1"}}
        mock_post = mocker.patch("connectors.einvoice_client.requests.post", return_value=mock_resp)

        from tools.allowance_tools import create_b2b_allowance
        result = create_b2b_allowance(
            allowance_number="ZZ00000001",
            allowance_date="20240115",
            seller_name="Seller Corp",
            seller_address="123 Main St",
            seller_person_in_charge="John",
            seller_telephone="02-12345678",
            seller_facsimile="02-12345679",
            buyer_identifier="87654321",
            buyer_name="Buyer Corp",
            allowance_type="1",
            items=[SAMPLE_ITEM_NAMED],
            tax_amount="10",
            total_amount="210",
        )
        called_body = json.loads(mock_post.call_args[1]["data"])
        inv = called_body["Invoice"]
        assert inv["INVOICE_CODE"] == "B0401"
        assert inv["ALLOWANCENUMBER"] == "ZZ00000001"
        assert inv["S_NAME"] == "Seller Corp"
        assert inv["S_ADDRESS"] == "123 Main St"
        assert inv["IDENTIFIER"] == "87654321"
        assert inv["PRODUCTITEM"] == [SAMPLE_ITEM_NAMED]
        assert result["Invoice"]["REPLY"] == "1"

    def test_b0401_uses_invoice_wrapper(self, mocker, mock_env):
        mock_resp = mocker.Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"Invoice": {"REPLY": "1"}}
        mock_post = mocker.patch("connectors.einvoice_client.requests.post", return_value=mock_resp)

        from tools.allowance_tools import create_b2b_allowance
        create_b2b_allowance(
            allowance_number="ZZ00000001",
            allowance_date="20240115",
            seller_name="Seller",
            seller_address="123 St",
            seller_person_in_charge="John",
            seller_telephone="02-12345678",
            seller_facsimile="02-12345679",
            buyer_identifier="87654321",
            buyer_name="Buyer",
            allowance_type="1",
            items=[SAMPLE_ITEM_NAMED],
            tax_amount="10",
            total_amount="210",
        )
        called_body = json.loads(mock_post.call_args[1]["data"])
        assert "Invoice" in called_body
        assert "Allowance" not in called_body


class TestVoidB2bAllowance:
    def test_b0501_uses_allowance_wrapper(self, mocker, mock_env):
        mock_resp = mocker.Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"Allowance": {"REPLY": "1"}}
        mock_post = mocker.patch("connectors.einvoice_client.requests.post", return_value=mock_resp)

        from tools.allowance_tools import void_b2b_allowance
        result = void_b2b_allowance(
            allowance_number="ZZ00000001",
            allowance_date="20240115",
            buyer_id="87654321",
            seller_id="12345678",
            cancel_date="20240120",
            cancel_time="100000",
            cancel_reason="Error",
        )
        called_body = json.loads(mock_post.call_args[1]["data"])
        assert "Allowance" in called_body
        assert "Invoice" not in called_body
        inv = called_body["Allowance"]
        assert inv["INVOICE_CODE"] == "B0501"
        assert inv["ALLOWANCENUMBER"] == "ZZ00000001"
        assert inv["BUYERID"] == "87654321"
        assert result["Allowance"]["REPLY"] == "1"


class TestCreateB2bExchangeAllowance:
    def test_b0101_payload_structure(self, mocker, mock_env):
        mock_resp = mocker.Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"Invoice": {"REPLY": "1"}}
        mock_post = mocker.patch("connectors.einvoice_client.requests.post", return_value=mock_resp)

        from tools.allowance_tools import create_b2b_exchange_allowance
        result = create_b2b_exchange_allowance(
            allowance_number="ZZ00000001",
            allowance_date="20240115",
            seller_identifier="12345678",
            seller_name="Seller Corp",
            seller_address="123 Main St",
            buyer_identifier="87654321",
            buyer_name="Buyer Corp",
            allowance_type="1",
            items=[SAMPLE_ITEM_NAMED],
            tax_amount="10",
            total_amount="210",
        )
        called_body = json.loads(mock_post.call_args[1]["data"])
        inv = called_body["Invoice"]
        assert inv["INVOICE_CODE"] == "B0101"
        assert inv["ALLOWANCENUMBER"] == "ZZ00000001"
        assert inv["Seller"]["Identifier"] == "12345678"
        assert inv["Seller"]["Address"] == "123 Main St"
        assert inv["Buyer"]["Identifier"] == "87654321"
        assert inv["PRODUCTITEM"] == [SAMPLE_ITEM_NAMED]
        assert result["Invoice"]["REPLY"] == "1"
