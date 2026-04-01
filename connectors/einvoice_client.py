"""Universal EC E-Invoice API connector — single POST endpoint."""

import json
import time
from datetime import datetime

import requests

from config.settings import get_base_url, get_credentials


class EInvoiceAPIError(Exception):
    def __init__(self, status_code: int, message: str, function_code: str = ""):
        self.status_code = status_code
        self.message = message
        self.function_code = function_code
        super().__init__(f"[{status_code}] {function_code}: {message}")


def _get_systime() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def post_einvoice(
    function_code: str,
    payload: dict,
    wrapper: str = "INDEX",
    retries: int = 3,
    timeout: int = 60,
) -> dict:
    url = get_base_url()
    creds = get_credentials()

    if wrapper == "INDEX":
        # Minimal required fields — individual tools add their specific fields via payload
        index_data = {
            "FUNCTIONCODE": function_code,
            "SELLERID": creds["SELLERID"],
            "POSID": creds["POSID"],
            "POSSN": creds["POSSN"],
            "SYSTIME": _get_systime(),
        }
        # A01/C01/Y01/Z21/Z22 need these extra defaults; Z11 does not
        if function_code in ("A01", "C01", "Y01", "Z21", "Z22"):
            index_data.update({
                "ACCOUNT": "0000000000000000",
                "APPID": "0000000000000000",
                "ServerType": "invioce_ml",
                "REPLY": "",
                "MESSAGE": "",
                "VERIONUPDATE": "",
                "EcrId": "",
                "APPVSERION": "",
            })
        index_data.update(payload)
        body = {"INDEX": index_data}
    elif wrapper == "Invoice":
        inner = {
            "POSSN": creds["POSSN"],
            "POSID": creds["POSID"],
            "SELLERID": creds["SELLERID"],
            "SYSTIME": _get_systime(),
            "ACCOUNT": "0000000000000000",
            "APPID": "0000000000000000",
            "ServerType": "invioce_ml",
            **payload,
        }
        body = {"Invoice": inner}
    elif wrapper == "Allowance":
        inner = {
            "POSSN": creds["POSSN"],
            "POSID": creds["POSID"],
            "SELLERID": creds["SELLERID"],
            "SYSTIME": _get_systime(),
            **payload,
        }
        body = {"Allowance": inner}
    else:
        raise ValueError(f"Unknown wrapper type: {wrapper}")

    headers = {"Content-Type": "application/json; charset=utf-8"}

    for attempt in range(retries):
        try:
            response = requests.post(
                url,
                data=json.dumps(body, ensure_ascii=False),
                headers=headers,
                timeout=timeout,
            )
            if response.status_code >= 400:
                raise EInvoiceAPIError(
                    status_code=response.status_code,
                    message=response.text[:500],
                    function_code=function_code,
                )
            return response.json()
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
            else:
                raise EInvoiceAPIError(
                    status_code=0,
                    message="Request failed after all retries (timeout/connection error)",
                    function_code=function_code,
                )
