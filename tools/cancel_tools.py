"""Cancel tools — C0701, B0701."""

from datetime import datetime
from typing import Annotated, Optional
from pydantic import Field
from app import mcp
from connectors.einvoice_client import post_einvoice
from config.settings import get_credentials


@mcp.tool()
def cancel_invoice(
    invoice_number: str = Field(description="Invoice number to cancel (註銷)."),
    invoice_date: str = Field(description="Original invoice date (YYYYMMDD)."),
    buyer_id: str = Field(description="Buyer identifier."),
    seller_id: str = Field(description="Seller identifier."),
    cancel_date: str = Field(description="Cancellation date (YYYYMMDD)."),
    cancel_time: str = Field(description="Cancellation time (HHmmss)."),
    cancel_reason: str = Field(description="Cancellation reason."),
    return_tax_document_number: Annotated[Optional[str], Field(description="Return/tax document number.")] = None,
    remark: Annotated[Optional[str], Field(description="Remark.")] = None,
) -> dict:
    """Cancel (註銷) an invoice (C0701). Returns the API response."""
    payload: dict = {
        "INVOICE_CODE": "C0701",
        "INVOICE_NUMBER": invoice_number,
        "INVOICE_DATE": invoice_date,
        "BUYERID": buyer_id,
        "SELLERID": seller_id,
        "CANCEL_DATE": cancel_date,
        "CANCEL_TIME": cancel_time,
        "CANCEL_REASON": cancel_reason,
    }
    if return_tax_document_number is not None:
        payload["RETURNTAXDOCUMENT_NUMBER"] = return_tax_document_number
    if remark is not None:
        payload["REMARK"] = remark
    return post_einvoice("C0701", payload, wrapper="Invoice")


@mcp.tool()
def batch_cancel_invoice(
    cancel_date: str = Field(description="Cancellation date (YYYYMMDD)."),
    cancel_time: str = Field(description="Cancellation time (HHmmss)."),
    cancel_reason: str = Field(description="Cancellation reason."),
    invoice_number: str = Field(description="Invoice number (A2, positional format)."),
    invoice_date: str = Field(description="Invoice date (A3)."),
    invoice_time: str = Field(description="Invoice time (A4)."),
    buyer_id: str = Field(description="Buyer identifier (A5)."),
    buyer_name: str = Field(description="Buyer name (A6)."),
    invoice_type: str = Field(description="Invoice type code (A22)."),
    donate_mark: str = Field(description="Donate mark (A24)."),
    print_mark: str = Field(description="Print mark (A28)."),
    random_number: str = Field(description="Random number (A30)."),
    items: list = Field(description="List of invoice line items in positional format (B). Each item: {B1, B2, B3, B5, B6, B7, B13}."),
    sales_amount: str = Field(description="Taxable sales amount (C1)."),
    free_tax: str = Field(description="Tax-exempt sales amount (C2)."),
    zero_tax: str = Field(description="Zero-tax-rate sales amount (C3)."),
    tax_type: str = Field(description="Tax type (C4)."),
    tax_rate: str = Field(description="Tax rate (C5)."),
    tax_amount: str = Field(description="Tax amount (C6)."),
    total: str = Field(description="Total amount including tax (C7)."),
    carrier_type: Annotated[Optional[str], Field(description="Carrier type (A25).")] = None,
    carrier_id1: Annotated[Optional[str], Field(description="Carrier ID primary (A26).")] = None,
    carrier_id2: Annotated[Optional[str], Field(description="Carrier ID secondary (A27).")] = None,
    donate_to: Annotated[Optional[str], Field(description="NPO ban love code (A29).")] = None,
    zero_tax_reason: Annotated[Optional[str], Field(description="Zero-tax-rate reason code (A31).")] = None,
    main_remark: Annotated[Optional[str], Field(description="Main remark (A16).")] = None,
    customs_clearance: Annotated[Optional[str], Field(description="Customs clearance mark (A17).")] = None,
    discount: Annotated[Optional[str], Field(description="Discount amount (C8).")] = None,
    original_currency_amount: Annotated[Optional[str], Field(description="Original currency amount (C9).")] = None,
    exchange_rate: Annotated[Optional[str], Field(description="Exchange rate (C10).")] = None,
    currency: Annotated[Optional[str], Field(description="Currency code (C11).")] = None,
) -> dict:
    """Batch cancel an invoice by re-submitting full invoice data with cancellation info (B0701). Returns the API response."""
    creds = get_credentials()
    payload: dict = {
        "INVOICE_CODE": "B0701",
        "CANCEL_DATE": cancel_date,
        "CANCEL_TIME": cancel_time,
        "CANCEL_REASON": cancel_reason,
        "A2": invoice_number,
        "A3": invoice_date,
        "A4": invoice_time,
        "A5": buyer_id,
        "A6": buyer_name,
        "A7": "", "A8": "", "A9": "", "A10": "", "A11": "", "A12": "", "A13": "",
        "A15": "", "A16": "", "A17": "", "A18": "", "A19": "", "A20": "", "A21": "",
        "A22": invoice_type,
        "A23": "",
        "A24": donate_mark,
        "A25": "", "A26": "", "A27": "",
        "A28": print_mark,
        "A29": "",
        "A30": random_number,
        "A31": "",
        "B": items,
        "C1": sales_amount,
        "C2": free_tax,
        "C3": zero_tax,
        "C4": tax_type,
        "C5": tax_rate,
        "C6": tax_amount,
        "C7": total,
        "C8": "", "C9": "", "C10": "0.00", "C11": "", "C12": "", "C13": "",
        "D1": creds["SELLERID"],
        "D2": creds["POSSN"],
        "D3": creds["POSID"],
        "D4": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "EcrId": "",
        "SellerName": "",
        "QRCodeASKey": "",
    }
    if carrier_type is not None:
        payload["A25"] = carrier_type
    if carrier_id1 is not None:
        payload["A26"] = carrier_id1
    if carrier_id2 is not None:
        payload["A27"] = carrier_id2
    if donate_to is not None:
        payload["A29"] = donate_to
    if zero_tax_reason is not None:
        payload["A31"] = zero_tax_reason
    if main_remark is not None:
        payload["A16"] = main_remark
    if customs_clearance is not None:
        payload["A17"] = customs_clearance
    if discount is not None:
        payload["C8"] = discount
    if original_currency_amount is not None:
        payload["C9"] = original_currency_amount
    if exchange_rate is not None:
        payload["C10"] = exchange_rate
    if currency is not None:
        payload["C11"] = currency
    return post_einvoice("B0701", payload, wrapper="Invoice")
