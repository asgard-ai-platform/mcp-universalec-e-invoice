"""B2B invoice tools — A0401, A0501, A0101, A0201."""

from typing import Annotated, Optional
from pydantic import Field
from app import mcp
from connectors.einvoice_client import post_einvoice


@mcp.tool()
def create_b2b_invoice(
    invoice_number: str = Field(description="Invoice number."),
    invoice_date: str = Field(description="Invoice date (YYYYMMDD)."),
    invoice_time: str = Field(description="Invoice time (HHmmss)."),
    seller_identifier: str = Field(description="Seller tax ID."),
    seller_name: str = Field(description="Seller name."),
    buyer_identifier: str = Field(description="Buyer tax ID."),
    buyer_name: str = Field(description="Buyer name."),
    invoice_type: str = Field(description="Invoice type code."),
    donate_mark: str = Field(description="Donate mark ('0'=no donate)."),
    print_mark: str = Field(description="Print mark ('Y' or 'N')."),
    items: list = Field(description="List of product items. Each item: {Description, Quantity, UnitPrice, TaxType, Amount, SequenceNumber, optional: Unit, Remark, RelateNumber}."),
    sales_amount: str = Field(description="Taxable sales amount."),
    tax_type: str = Field(description="Tax type."),
    tax_rate: str = Field(description="Tax rate."),
    tax_amount: str = Field(description="Tax amount."),
    total_amount: str = Field(description="Total amount including tax."),
    seller_address: Annotated[Optional[str], Field(description="Seller address.")] = None,
    seller_person_in_charge: Annotated[Optional[str], Field(description="Seller person in charge.")] = None,
    seller_telephone: Annotated[Optional[str], Field(description="Seller telephone number.")] = None,
    seller_facsimile: Annotated[Optional[str], Field(description="Seller facsimile number.")] = None,
    seller_email: Annotated[Optional[str], Field(description="Seller email address.")] = None,
    seller_customer_number: Annotated[Optional[str], Field(description="Seller customer number.")] = None,
    seller_role_remark: Annotated[Optional[str], Field(description="Seller role remark.")] = None,
    buyer_address: Annotated[Optional[str], Field(description="Buyer address.")] = None,
    buyer_person_in_charge: Annotated[Optional[str], Field(description="Buyer person in charge.")] = None,
    buyer_telephone: Annotated[Optional[str], Field(description="Buyer telephone number.")] = None,
    buyer_facsimile: Annotated[Optional[str], Field(description="Buyer facsimile number.")] = None,
    buyer_email: Annotated[Optional[str], Field(description="Buyer email address.")] = None,
    buyer_customer_number: Annotated[Optional[str], Field(description="Buyer customer number.")] = None,
    buyer_role_remark: Annotated[Optional[str], Field(description="Buyer role remark.")] = None,
    check_number: Annotated[Optional[str], Field(description="Check number.")] = None,
    buyer_remark: Annotated[Optional[str], Field(description="Buyer remark.")] = None,
    main_remark: Annotated[Optional[str], Field(description="Main remark.")] = None,
    customs_clearance_mark: Annotated[Optional[str], Field(description="Customs clearance mark.")] = None,
    zero_tax_rate_reason: Annotated[Optional[str], Field(description="Zero-tax-rate reason code.")] = None,
    bonded_area_confirm: Annotated[Optional[str], Field(description="Bonded area confirm.")] = None,
    discount_amount: Annotated[Optional[str], Field(description="Discount amount.")] = None,
    original_currency_amount: Annotated[Optional[str], Field(description="Original currency amount.")] = None,
    exchange_rate: Annotated[Optional[str], Field(description="Exchange rate.")] = None,
    currency: Annotated[Optional[str], Field(description="Currency code (e.g. 'USD').")] = None,
) -> dict:
    """Create a B2B invoice using named nested format (A0401). Returns the API response."""
    seller: dict = {"Identifier": seller_identifier, "Name": seller_name}
    if seller_address is not None:
        seller["Address"] = seller_address
    if seller_person_in_charge is not None:
        seller["PersonInCharge"] = seller_person_in_charge
    if seller_telephone is not None:
        seller["TelephoneNumber"] = seller_telephone
    if seller_facsimile is not None:
        seller["FacsimileNumber"] = seller_facsimile
    if seller_email is not None:
        seller["EmailAddress"] = seller_email
    if seller_customer_number is not None:
        seller["CustomerNumber"] = seller_customer_number
    if seller_role_remark is not None:
        seller["RoleRemark"] = seller_role_remark

    buyer: dict = {"Identifier": buyer_identifier, "Name": buyer_name}
    if buyer_address is not None:
        buyer["Address"] = buyer_address
    if buyer_person_in_charge is not None:
        buyer["PersonInCharge"] = buyer_person_in_charge
    if buyer_telephone is not None:
        buyer["TelephoneNumber"] = buyer_telephone
    if buyer_facsimile is not None:
        buyer["FacsimileNumber"] = buyer_facsimile
    if buyer_email is not None:
        buyer["EmailAddress"] = buyer_email
    if buyer_customer_number is not None:
        buyer["CustomerNumber"] = buyer_customer_number
    if buyer_role_remark is not None:
        buyer["RoleRemark"] = buyer_role_remark

    main: dict = {
        "InvoiceNumber": invoice_number,
        "InvoiceDate": invoice_date,
        "InvoiceTime": invoice_time,
        "Seller": seller,
        "Buyer": buyer,
        "InvoiceType": invoice_type,
        "DonateMark": donate_mark,
        "PrintMark": print_mark,
    }
    if check_number is not None:
        main["CheckNumber"] = check_number
    if buyer_remark is not None:
        main["BuyerRemark"] = buyer_remark
    if main_remark is not None:
        main["MainRemark"] = main_remark
    if customs_clearance_mark is not None:
        main["CustomsClearanceMark"] = customs_clearance_mark
    if zero_tax_rate_reason is not None:
        main["ZeroTaxRateReason"] = zero_tax_rate_reason
    if bonded_area_confirm is not None:
        main["BondedAreaConfirm"] = bonded_area_confirm

    amount: dict = {
        "SalesAmount": sales_amount,
        "TaxType": tax_type,
        "TaxRate": tax_rate,
        "TaxAmount": tax_amount,
        "TotalAmount": total_amount,
    }
    if discount_amount is not None:
        amount["DiscountAmount"] = discount_amount
    if original_currency_amount is not None:
        amount["OriginalCurrencyAmount"] = original_currency_amount
    if exchange_rate is not None:
        amount["ExchangeRate"] = exchange_rate
    if currency is not None:
        amount["Currency"] = currency

    payload = {
        "INVOICE_CODE": "A0401",
        "Main": main,
        "Details": {"ProductItem": items},
        "Amount": amount,
    }
    return post_einvoice("A0401", payload, wrapper="Invoice")


@mcp.tool()
def void_b2b_invoice(
    cancel_invoice_number: str = Field(description="Invoice number to void."),
    invoice_date: str = Field(description="Original invoice date (YYYYMMDD)."),
    buyer_id: str = Field(description="Buyer tax ID."),
    seller_id: str = Field(description="Seller tax ID."),
    cancel_date: str = Field(description="Cancellation date (YYYYMMDD)."),
    cancel_time: str = Field(description="Cancellation time (HHmmss)."),
    cancel_reason: str = Field(description="Cancellation reason."),
    return_tax_document_number: Annotated[Optional[str], Field(description="Return/tax document number.")] = None,
    remark: Annotated[Optional[str], Field(description="Remark.")] = None,
    buyer_email_address: Annotated[Optional[str], Field(description="Buyer email address for notification.")] = None,
) -> dict:
    """Void (invalidate) a B2B invoice (A0501). Returns the API response."""
    payload: dict = {
        "INVOICE_CODE": "A0501",
        "CancelInvoiceNumber": cancel_invoice_number,
        "InvoiceDate": invoice_date,
        "BuyerId": buyer_id,
        "SellerId": seller_id,
        "CancelDate": cancel_date,
        "CancelTime": cancel_time,
        "CancelReason": cancel_reason,
    }
    if return_tax_document_number is not None:
        payload["ReturnTaxDocumentNumber"] = return_tax_document_number
    if remark is not None:
        payload["Remark"] = remark
    if buyer_email_address is not None:
        payload["B_EMAIL_ADDRESS"] = buyer_email_address
    return post_einvoice("A0501", payload, wrapper="Invoice")


@mcp.tool()
def create_b2b_exchange_invoice(
    invoice_number: str = Field(description="Invoice number."),
    invoice_date: str = Field(description="Invoice date (YYYYMMDD)."),
    invoice_time: str = Field(description="Invoice time (HHmmss)."),
    seller_identifier: str = Field(description="Seller tax ID."),
    seller_name: str = Field(description="Seller name."),
    seller_address: str = Field(description="Seller address (mandatory for exchange invoices)."),
    buyer_identifier: str = Field(description="Buyer tax ID."),
    buyer_name: str = Field(description="Buyer name."),
    invoice_type: str = Field(description="Invoice type code."),
    donate_mark: str = Field(description="Donate mark ('0'=no donate)."),
    print_mark: str = Field(description="Print mark ('Y' or 'N')."),
    items: list = Field(description="List of product items. Each item: {Description, Quantity, UnitPrice, DTaxType, Amount, SequenceNumber, optional: Unit, Remark, RelateNumber}."),
    sales_amount: str = Field(description="Taxable sales amount."),
    tax_type: str = Field(description="Tax type."),
    tax_rate: str = Field(description="Tax rate."),
    tax_amount: str = Field(description="Tax amount."),
    total_amount: str = Field(description="Total amount including tax."),
    seller_person_in_charge: Annotated[Optional[str], Field(description="Seller person in charge.")] = None,
    seller_telephone: Annotated[Optional[str], Field(description="Seller telephone number.")] = None,
    seller_facsimile: Annotated[Optional[str], Field(description="Seller facsimile number.")] = None,
    seller_email: Annotated[Optional[str], Field(description="Seller email address.")] = None,
    buyer_address: Annotated[Optional[str], Field(description="Buyer address.")] = None,
    check_number: Annotated[Optional[str], Field(description="Check number.")] = None,
    main_remark: Annotated[Optional[str], Field(description="Main remark.")] = None,
    customs_clearance_mark: Annotated[Optional[str], Field(description="Customs clearance mark.")] = None,
    zero_tax_rate_reason: Annotated[Optional[str], Field(description="Zero-tax-rate reason code.")] = None,
    bonded_area_confirm: Annotated[Optional[str], Field(description="Bonded area confirm.")] = None,
    discount_amount: Annotated[Optional[str], Field(description="Discount amount.")] = None,
    original_currency_amount: Annotated[Optional[str], Field(description="Original currency amount.")] = None,
    exchange_rate: Annotated[Optional[str], Field(description="Exchange rate.")] = None,
    currency: Annotated[Optional[str], Field(description="Currency code (e.g. 'USD').")] = None,
) -> dict:
    """Create a B2B exchange invoice (A0101). Seller address is mandatory. Item tax type field is DTaxType. Returns the API response."""
    seller: dict = {
        "Identifier": seller_identifier,
        "Name": seller_name,
        "Address": seller_address,
    }
    if seller_person_in_charge is not None:
        seller["PersonInCharge"] = seller_person_in_charge
    if seller_telephone is not None:
        seller["TelephoneNumber"] = seller_telephone
    if seller_facsimile is not None:
        seller["FacsimileNumber"] = seller_facsimile
    if seller_email is not None:
        seller["EmailAddress"] = seller_email

    buyer: dict = {"Identifier": buyer_identifier, "Name": buyer_name}
    if buyer_address is not None:
        buyer["Address"] = buyer_address

    main: dict = {
        "InvoiceNumber": invoice_number,
        "InvoiceDate": invoice_date,
        "InvoiceTime": invoice_time,
        "Seller": seller,
        "Buyer": buyer,
        "InvoiceType": invoice_type,
        "DonateMark": donate_mark,
        "PrintMark": print_mark,
    }
    if check_number is not None:
        main["CheckNumber"] = check_number
    if main_remark is not None:
        main["MainRemark"] = main_remark
    if customs_clearance_mark is not None:
        main["CustomsClearanceMark"] = customs_clearance_mark
    if zero_tax_rate_reason is not None:
        main["ZeroTaxRateReason"] = zero_tax_rate_reason
    if bonded_area_confirm is not None:
        main["BondedAreaConfirm"] = bonded_area_confirm

    amount: dict = {
        "SalesAmount": sales_amount,
        "TaxType": tax_type,
        "TaxRate": tax_rate,
        "TaxAmount": tax_amount,
        "TotalAmount": total_amount,
    }
    if discount_amount is not None:
        amount["DiscountAmount"] = discount_amount
    if original_currency_amount is not None:
        amount["OriginalCurrencyAmount"] = original_currency_amount
    if exchange_rate is not None:
        amount["ExchangeRate"] = exchange_rate
    if currency is not None:
        amount["Currency"] = currency

    payload = {
        "INVOICE_CODE": "A0101",
        "Main": main,
        "Details": {"ProductItem": items},
        "Amount": amount,
    }
    return post_einvoice("A0101", payload, wrapper="Invoice")


@mcp.tool()
def void_b2b_exchange_invoice(
    cancel_invoice_number: str = Field(description="Exchange invoice number to void."),
    invoice_date: str = Field(description="Original invoice date (YYYYMMDD)."),
    buyer_id: str = Field(description="Buyer tax ID."),
    seller_id: str = Field(description="Seller tax ID."),
    cancel_date: str = Field(description="Cancellation date (YYYYMMDD)."),
    cancel_time: str = Field(description="Cancellation time (HHmmss)."),
    cancel_reason: str = Field(description="Cancellation reason."),
    return_tax_document_number: Annotated[Optional[str], Field(description="Return/tax document number.")] = None,
    remark: Annotated[Optional[str], Field(description="Remark.")] = None,
) -> dict:
    """Void (invalidate) a B2B exchange invoice (A0201). Returns the API response."""
    payload: dict = {
        "INVOICE_CODE": "A0201",
        "CancelInvoiceNumber": cancel_invoice_number,
        "InvoiceDate": invoice_date,
        "BuyerId": buyer_id,
        "SellerId": seller_id,
        "CancelDate": cancel_date,
        "CancelTime": cancel_time,
        "CancelReason": cancel_reason,
    }
    if return_tax_document_number is not None:
        payload["ReturnTaxDocumentNumber"] = return_tax_document_number
    if remark is not None:
        payload["Remark"] = remark
    return post_einvoice("A0201", payload, wrapper="Invoice")
