"""B2C invoice tools — C0401, C0401N, C0501."""

from datetime import datetime
from typing import Annotated, Optional
from pydantic import Field
from app import mcp
from connectors.einvoice_client import post_einvoice
from config.settings import get_credentials


@mcp.tool()
def create_b2c_invoice(
    invoice_number: str = Field(description="Invoice number (e.g. 'AB12345678')."),
    invoice_date: str = Field(description="Invoice date (YYYYMMDD)."),
    invoice_time: str = Field(description="Invoice time (HHmmss)."),
    buyer_id: str = Field(description="Buyer identifier (tax ID or empty string)."),
    buyer_name: str = Field(description="Buyer name."),
    invoice_type: str = Field(description="Invoice type code (e.g. '07')."),
    donate_mark: str = Field(description="Donate mark ('1'=donate, '0'=no)."),
    print_mark: str = Field(description="Print mark ('Y' or 'N')."),
    random_number: str = Field(description="4-digit random number."),
    items: list = Field(description="List of invoice line items. Each item: {B1: seq, B2: description, B3: qty, B5: unit_price, B6: amount, B7: tax_type, B13: tax_amount}."),
    sales_amount: str = Field(description="Taxable sales amount."),
    free_tax: str = Field(description="Tax-exempt sales amount."),
    zero_tax: str = Field(description="Zero-tax-rate sales amount."),
    tax_type: str = Field(description="Tax type ('1'=taxable, '2'=zero-rate, '3'=exempt, '9'=mixed)."),
    tax_rate: str = Field(description="Tax rate (e.g. '0.05')."),
    tax_amount: str = Field(description="Tax amount."),
    total: str = Field(description="Total amount including tax."),
    carrier_type: Annotated[Optional[str], Field(description="Carrier type (e.g. '3J0002' for mobile barcode).")] = None,
    carrier_id1: Annotated[Optional[str], Field(description="Carrier ID primary (encoded).")] = None,
    carrier_id2: Annotated[Optional[str], Field(description="Carrier ID secondary (plain).")] = None,
    donate_to: Annotated[Optional[str], Field(description="NPO ban (love code) when donating.")] = None,
    zero_tax_reason: Annotated[Optional[str], Field(description="Zero-tax-rate reason code.")] = None,
    main_remark: Annotated[Optional[str], Field(description="Main remark.")] = None,
    customs_clearance: Annotated[Optional[str], Field(description="Customs clearance mark.")] = None,
    discount: Annotated[Optional[str], Field(description="Discount amount.")] = None,
    original_currency_amount: Annotated[Optional[str], Field(description="Original currency amount.")] = None,
    exchange_rate: Annotated[Optional[str], Field(description="Exchange rate.")] = None,
    currency: Annotated[Optional[str], Field(description="Currency code (e.g. 'USD').")] = None,
) -> dict:
    """Create a B2C invoice using positional field format (C0401). Returns the API response."""
    creds = get_credentials()
    payload: dict = {
        "A1": "C0401",
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
    return post_einvoice("C0401", payload, wrapper="Invoice")


@mcp.tool()
def create_b2c_invoice_named(
    invoice_number: str = Field(description="Invoice number."),
    invoice_date: str = Field(description="Invoice date (YYYYMMDD)."),
    invoice_time: str = Field(description="Invoice time (HHmmss)."),
    seller_identifier: str = Field(description="Seller tax ID."),
    buyer_identifier: str = Field(description="Buyer tax ID (or empty string)."),
    buyer_name: str = Field(description="Buyer name."),
    invoice_type: str = Field(description="Invoice type code."),
    donate_mark: str = Field(description="Donate mark ('1'=donate, '0'=no)."),
    print_mark: str = Field(description="Print mark ('Y' or 'N')."),
    random_number: str = Field(description="4-digit random number."),
    items: list = Field(description="List of product items. Each item: {Description, Quantity, UnitPrice, TaxType, Amount, SequenceNumber}."),
    sales_amount: str = Field(description="Taxable sales amount."),
    free_tax_sales_amount: str = Field(description="Tax-exempt sales amount."),
    zero_tax_sales_amount: str = Field(description="Zero-tax-rate sales amount."),
    amount_tax_type: str = Field(description="Tax type for amount section."),
    tax_rate: str = Field(description="Tax rate."),
    tax_amount: str = Field(description="Tax amount."),
    total_amount: str = Field(description="Total amount including tax."),
    carrier_type: Annotated[Optional[str], Field(description="Carrier type code.")] = None,
    carrier_id1: Annotated[Optional[str], Field(description="Carrier ID primary (encoded).")] = None,
    carrier_id2: Annotated[Optional[str], Field(description="Carrier ID secondary (plain).")] = None,
    npo_ban: Annotated[Optional[str], Field(description="NPO ban (love code) when donating.")] = None,
    zero_tax_rate_reason: Annotated[Optional[str], Field(description="Zero-tax-rate reason code.")] = None,
    main_remark: Annotated[Optional[str], Field(description="Main remark.")] = None,
) -> dict:
    """Create a B2C invoice using named nested field format (C0401N). Returns the API response."""
    main: dict = {
        "InvoiceNumber": invoice_number,
        "InvoiceDate": invoice_date,
        "InvoiceTime": invoice_time,
        "Seller": {"Identifier": seller_identifier},
        "Buyer": {"Identifier": buyer_identifier, "Name": buyer_name},
        "InvoiceType": invoice_type,
        "DonateMark": donate_mark,
        "PrintMark": print_mark,
        "RandomNumber": random_number,
    }
    if carrier_type is not None:
        main["CarrierType"] = carrier_type
    if carrier_id1 is not None:
        main["CarrierID1"] = carrier_id1
    if carrier_id2 is not None:
        main["CarrierID2"] = carrier_id2
    if npo_ban is not None:
        main["NPOBan"] = npo_ban
    if zero_tax_rate_reason is not None:
        main["ZeroTaxRateReason"] = zero_tax_rate_reason
    if main_remark is not None:
        main["MainRemark"] = main_remark

    payload = {
        "INVOICE_CODE": "C0401N",
        "Main": main,
        "Details": {"ProductItem": items},
        "Amount": {
            "SalesAmount": sales_amount,
            "FreeTaxSalesAmount": free_tax_sales_amount,
            "ZeroTaxSalesAmount": zero_tax_sales_amount,
            "TaxType": amount_tax_type,
            "TaxRate": tax_rate,
            "TaxAmount": tax_amount,
            "TotalAmount": total_amount,
        },
    }
    return post_einvoice("C0401N", payload, wrapper="Invoice")


@mcp.tool()
def void_b2c_invoice(
    invoice_number: str = Field(description="Invoice number to void."),
    invoice_date: str = Field(description="Original invoice date (YYYYMMDD)."),
    buyer_id: str = Field(description="Buyer identifier."),
    seller_id: str = Field(description="Seller identifier."),
    cancel_date: str = Field(description="Cancellation date (YYYYMMDD)."),
    cancel_time: str = Field(description="Cancellation time (HHmmss)."),
    cancel_reason: str = Field(description="Cancellation reason."),
    return_tax_document_number: Annotated[Optional[str], Field(description="Return/tax document number.")] = None,
    remark: Annotated[Optional[str], Field(description="Remark.")] = None,
) -> dict:
    """Void (invalidate) a B2C invoice (C0501). Returns the API response."""
    payload: dict = {
        "INVOICE_CODE": "C0501",
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
    return post_einvoice("C0501", payload, wrapper="Invoice")
