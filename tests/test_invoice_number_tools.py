import json


class TestGetInvoiceNumbers:
    def test_a01_sends_correct_functioncode(self, mocker, mock_env):
        mock_resp = mocker.Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "INDEX": {
                "FUNCTIONCODE": "A01",
                "REPLY": "1",
                "MESSAGE": "成功",
                "TAXMONTH": "10708",
                "INVOICEHEADER": "DC",
                "INVOICESTART": "51705750",
                "INVOICEEND": "51705799",
                "QRCodeASKey": "5F2BF5EEA62517788999A08024437",
                "TYPE": "03",
            }
        }
        mock_post = mocker.patch("connectors.einvoice_client.requests.post", return_value=mock_resp)

        from tools.invoice_number_tools import get_invoice_numbers
        result = get_invoice_numbers()
        assert result["INDEX"]["REPLY"] == "1"
        assert result["INDEX"]["INVOICEHEADER"] == "DC"
        called_body = json.loads(mock_post.call_args[1]["data"])
        assert called_body["INDEX"]["FUNCTIONCODE"] == "A01"

    def test_a01_with_optional_params(self, mocker, mock_env):
        mock_resp = mocker.Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"INDEX": {"REPLY": "1"}}
        mock_post = mocker.patch("connectors.einvoice_client.requests.post", return_value=mock_resp)

        from tools.invoice_number_tools import get_invoice_numbers
        get_invoice_numbers(tax_month="11304", invoice_header="DC")
        called_body = json.loads(mock_post.call_args[1]["data"])
        assert called_body["INDEX"]["TAXMONTH"] == "11304"
        assert called_body["INDEX"]["INVOICEHEADER"] == "DC"


class TestGetNextPeriodNumbers:
    def test_c01(self, mocker, mock_env):
        mock_resp = mocker.Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"INDEX": {"FUNCTIONCODE": "C01", "REPLY": "1", "INVOICEHEADER": "KK"}}
        mock_post = mocker.patch("connectors.einvoice_client.requests.post", return_value=mock_resp)

        from tools.invoice_number_tools import get_next_period_numbers
        result = get_next_period_numbers()
        called_body = json.loads(mock_post.call_args[1]["data"])
        assert called_body["INDEX"]["FUNCTIONCODE"] == "C01"
        assert result["INDEX"]["REPLY"] == "1"


class TestGetInvoiceNumbersExpanded:
    def test_z21(self, mocker, mock_env):
        mock_resp = mocker.Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "INDEX": {
                "FUNCTIONCODE": "Z21",
                "REPLY": "1",
                "INVOICEDATA": [
                    {"INVOICE_NUMBER": "BX00000000", "AESKEY": "abc==", "RANDOMNUMBER": "1234", "TAXMONTH": "10806"}
                ],
            }
        }
        mock_post = mocker.patch("connectors.einvoice_client.requests.post", return_value=mock_resp)

        from tools.invoice_number_tools import get_invoice_numbers_expanded
        result = get_invoice_numbers_expanded()
        called_body = json.loads(mock_post.call_args[1]["data"])
        assert called_body["INDEX"]["FUNCTIONCODE"] == "Z21"
        assert len(result["INDEX"]["INVOICEDATA"]) == 1


class TestGetNextPeriodNumbersExpanded:
    def test_z22(self, mocker, mock_env):
        mock_resp = mocker.Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"INDEX": {"FUNCTIONCODE": "Z22", "REPLY": "1", "INVOICEDATA": []}}
        mock_post = mocker.patch("connectors.einvoice_client.requests.post", return_value=mock_resp)

        from tools.invoice_number_tools import get_next_period_numbers_expanded
        result = get_next_period_numbers_expanded()
        called_body = json.loads(mock_post.call_args[1]["data"])
        assert called_body["INDEX"]["FUNCTIONCODE"] == "Z22"
