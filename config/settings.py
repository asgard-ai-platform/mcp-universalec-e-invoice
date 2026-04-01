import os
from dotenv import load_dotenv

load_dotenv()


def get_base_url() -> str:
    url = os.environ.get("EINVOICE_BASE_URL")
    if not url:
        raise RuntimeError(
            "Missing EINVOICE_BASE_URL. Set it in .env or environment.\n"
            "  Example: EINVOICE_BASE_URL=https://epostw.einvoice.com.tw/GetInvoice.ashx"
        )
    return url


def get_credentials() -> dict:
    seller_id = os.environ.get("EINVOICE_SELLER_ID")
    pos_id = os.environ.get("EINVOICE_POS_ID")
    pos_sn = os.environ.get("EINVOICE_POS_SN")
    if not seller_id:
        raise RuntimeError("Missing EINVOICE_SELLER_ID environment variable.")
    if not pos_id:
        raise RuntimeError("Missing EINVOICE_POS_ID environment variable.")
    if not pos_sn:
        raise RuntimeError("Missing EINVOICE_POS_SN environment variable.")
    return {"SELLERID": seller_id, "POSID": pos_id, "POSSN": pos_sn}
