"""Allowance tools — D0401, D0401N, D0501, B0401, B0501, B0101."""

from typing import Annotated, Optional
from pydantic import Field
from app import mcp
from connectors.einvoice_client import post_einvoice


@mcp.tool()
def create_b2c_allowance(
    allowance_number: str = Field(description="Allowance number."),
    allowance_date: str = Field(description="Allowance date (YYYYMMDD)."),
    buyer_id: str = Field(description="Buyer identifier (tax ID or empty string)."),
    buyer_name: str = Field(description="Buyer name."),
    allowance_type: str = Field(description="Allowance type ('2'=seller notice)."),
    items: list = Field(description="List of allowance items. Each item: {D1: seq, D2: original_date, D3: original_inv_number, D4: seq_number, D5: description, D6: qty, D8: unit_price, D9: amount, D10: tax, D11: tax_type}."),
    tax_amount: str = Field(description="Tax amount (C2)."),
    total_amount: str = Field(description="Total amount (C3)."),
    buyer_address: Annotated[Optional[str], Field(description="Buyer address (B3).")] = None,
    buyer_person_in_charge: Annotated[Optional[str], Field(description="Buyer person in charge (B4).")] = None,
    buyer_telephone: Annotated[Optional[str], Field(description="Buyer telephone (B5).")] = None,
    buyer_facsimile: Annotated[Optional[str], Field(description="Buyer facsimile (B6).")] = None,
    buyer_email: Annotated[Optional[str], Field(description="Buyer email (B7).")] = None,
    buyer_customer_number: Annotated[Optional[str], Field(description="Buyer customer number (B8).")] = None,
    buyer_role_remark: Annotated[Optional[str], Field(description="Buyer role remark (B9).")] = None,
    original_seller_id: Annotated[Optional[str], Field(description="Original seller ID (C4).")] = None,
    original_buyer_id: Annotated[Optional[str], Field(description="Original buyer ID (C5).")] = None,
) -> dict:
    """Create a B2C allowance using positional field format (D0401). Returns the API response."""
    payload: dict = {
        "DISCOUNT_CODE": "D0401",
        "A1": allowance_number,
        "A2": allowance_date,
        "B1": buyer_id,
        "B2": buyer_name,
        "C1": allowance_type,
        "C2": tax_amount,
        "C3": total_amount,
        "D": items,
    }
    if buyer_address is not None:
        payload["B3"] = buyer_address
    if buyer_person_in_charge is not None:
        payload["B4"] = buyer_person_in_charge
    if buyer_telephone is not None:
        payload["B5"] = buyer_telephone
    if buyer_facsimile is not None:
        payload["B6"] = buyer_facsimile
    if buyer_email is not None:
        payload["B7"] = buyer_email
    if buyer_customer_number is not None:
        payload["B8"] = buyer_customer_number
    if buyer_role_remark is not None:
        payload["B9"] = buyer_role_remark
    if original_seller_id is not None:
        payload["C4"] = original_seller_id
    if original_buyer_id is not None:
        payload["C5"] = original_buyer_id
    return post_einvoice("D0401", payload, wrapper="Invoice")


@mcp.tool()
def create_b2c_allowance_named(
    allowance_number: str = Field(description="Allowance number."),
    allowance_date: str = Field(description="Allowance date (YYYYMMDD)."),
    buyer_identifier: str = Field(description="Buyer identifier (tax ID or empty string)."),
    buyer_name: str = Field(description="Buyer name."),
    allowance_type: str = Field(description="Allowance type ('2'=seller notice)."),
    items: list = Field(description="List of product items. Each item: {ORIGINALINVOICEDATE, ORIGINALINVOICENUMBER, ALLOWANCESEQUENCENUMBER, ORIGINALDESCRIPTION, QUANTITY, UNITPRICE, AMOUNT, TAX, TAXTYPE, optional: UNIT, ORIGINALSEQUENCENUMBER}."),
    tax_amount: str = Field(description="Tax amount."),
    total_amount: str = Field(description="Total amount."),
    original_invoice_seller_id: Annotated[Optional[str], Field(description="Original invoice seller ID.")] = None,
    original_invoice_buyer_id: Annotated[Optional[str], Field(description="Original invoice buyer ID.")] = None,
    address: Annotated[Optional[str], Field(description="Buyer address.")] = None,
    person_in_charge: Annotated[Optional[str], Field(description="Buyer person in charge.")] = None,
    telephone_number: Annotated[Optional[str], Field(description="Buyer telephone number.")] = None,
    facsimile_number: Annotated[Optional[str], Field(description="Buyer facsimile number.")] = None,
    email_address: Annotated[Optional[str], Field(description="Buyer email address.")] = None,
    customer_number: Annotated[Optional[str], Field(description="Buyer customer number.")] = None,
    role_remark: Annotated[Optional[str], Field(description="Buyer role remark.")] = None,
) -> dict:
    """Create a B2C allowance using named field format (D0401N). Returns the API response."""
    payload: dict = {
        "INVOICE_CODE": "D0401N",
        "ALLOWANCENUMBER": allowance_number,
        "ALLOWANCEDATE": allowance_date,
        "IDENTIFIER": buyer_identifier,
        "NAME": buyer_name,
        "ALLOWANCETYPE": allowance_type,
        "PRODUCTITEM": items,
        "TAXAMOUNT": tax_amount,
        "TOTALAMOUNT": total_amount,
    }
    if original_invoice_seller_id is not None:
        payload["ORIGINALINVOICESELLERID"] = original_invoice_seller_id
    if original_invoice_buyer_id is not None:
        payload["ORIGINALINVOICEBUYERID"] = original_invoice_buyer_id
    if address is not None:
        payload["ADDRESS"] = address
    if person_in_charge is not None:
        payload["PERSONINCHARGE"] = person_in_charge
    if telephone_number is not None:
        payload["TELEPHONENUMBER"] = telephone_number
    if facsimile_number is not None:
        payload["FACSIMILENUMBER"] = facsimile_number
    if email_address is not None:
        payload["EMAILADDRESS"] = email_address
    if customer_number is not None:
        payload["CUSTOMERNUMBER"] = customer_number
    if role_remark is not None:
        payload["ROLEREMARK"] = role_remark
    return post_einvoice("D0401N", payload, wrapper="Invoice")


@mcp.tool()
def void_b2c_allowance(
    allowance_number: str = Field(description="Allowance number to void."),
    allowance_date: str = Field(description="Original allowance date (YYYYMMDD)."),
    buyer_id: str = Field(description="Buyer identifier."),
    seller_id: str = Field(description="Seller identifier."),
    cancel_date: str = Field(description="Cancellation date (YYYYMMDD)."),
    cancel_time: str = Field(description="Cancellation time (HHmmss)."),
    cancel_reason: str = Field(description="Cancellation reason."),
    return_tax_document_number: Annotated[Optional[str], Field(description="Return/tax document number.")] = None,
    remark: Annotated[Optional[str], Field(description="Remark.")] = None,
    allowance_type: Annotated[Optional[str], Field(description="Allowance type.")] = None,
) -> dict:
    """Void (invalidate) a B2C allowance (D0501). Returns the API response."""
    payload: dict = {
        "INVOICE_CODE": "D0501",
        "INVOICE_NUMBER": allowance_number,
        "INVOICE_DATE": allowance_date,
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
    if allowance_type is not None:
        payload["ALLOWANCETYPE"] = allowance_type
    return post_einvoice("D0501", payload, wrapper="Invoice")


@mcp.tool()
def create_b2b_allowance(
    allowance_number: str = Field(description="Allowance number."),
    allowance_date: str = Field(description="Allowance date (YYYYMMDD)."),
    seller_name: str = Field(description="Seller name."),
    seller_address: str = Field(description="Seller address (mandatory)."),
    buyer_identifier: str = Field(description="Buyer tax ID."),
    buyer_name: str = Field(description="Buyer name."),
    allowance_type: str = Field(description="Allowance type."),
    items: list = Field(description="List of product items. Each item: {ALLOWANCESEQUENCENUMBER, ORIGINALINVOICEDATE, ORIGINALINVOICENUMBER, ORIGINALDESCRIPTION, QUANTITY, UNITPRICE, AMOUNT, TAX, TAXTYPE, optional: UNIT, ORIGINALSEQUENCENUMBER}."),
    tax_amount: str = Field(description="Tax amount."),
    total_amount: str = Field(description="Total amount."),
    seller_person_in_charge: Annotated[Optional[str], Field(description="Seller person in charge (S_PERSONINCHARGE).")] = None,
    seller_telephone: Annotated[Optional[str], Field(description="Seller telephone (S_TELEPHONENUMBER).")] = None,
    seller_facsimile: Annotated[Optional[str], Field(description="Seller facsimile (S_FACSIMILENUMBER).")] = None,
    seller_email: Annotated[Optional[str], Field(description="Seller email address.")] = None,
    seller_customer_number: Annotated[Optional[str], Field(description="Seller customer number.")] = None,
    seller_role_remark: Annotated[Optional[str], Field(description="Seller role remark.")] = None,
    original_invoice_seller_id: Annotated[Optional[str], Field(description="Original invoice seller ID.")] = None,
    original_invoice_buyer_id: Annotated[Optional[str], Field(description="Original invoice buyer ID.")] = None,
    buyer_address: Annotated[Optional[str], Field(description="Buyer address.")] = None,
    buyer_person_in_charge: Annotated[Optional[str], Field(description="Buyer person in charge.")] = None,
    buyer_telephone: Annotated[Optional[str], Field(description="Buyer telephone number.")] = None,
    buyer_facsimile: Annotated[Optional[str], Field(description="Buyer facsimile number.")] = None,
    buyer_email: Annotated[Optional[str], Field(description="Buyer email address.")] = None,
    buyer_customer_number: Annotated[Optional[str], Field(description="Buyer customer number.")] = None,
    buyer_role_remark: Annotated[Optional[str], Field(description="Buyer role remark.")] = None,
) -> dict:
    """Create a B2B allowance (B0401). Seller address is mandatory. Returns the API response."""
    payload: dict = {
        "INVOICE_CODE": "B0401",
        "ALLOWANCENUMBER": allowance_number,
        "ALLOWANCEDATE": allowance_date,
        "S_NAME": seller_name,
        "S_ADDRESS": seller_address,
        "IDENTIFIER": buyer_identifier,
        "NAME": buyer_name,
        "ALLOWANCETYPE": allowance_type,
        "PRODUCTITEM": items,
        "TAXAMOUNT": tax_amount,
        "TOTALAMOUNT": total_amount,
    }
    if seller_person_in_charge is not None:
        payload["S_PERSONINCHARGE"] = seller_person_in_charge
    if seller_telephone is not None:
        payload["S_TELEPHONENUMBER"] = seller_telephone
    if seller_facsimile is not None:
        payload["S_FACSIMILENUMBER"] = seller_facsimile
    if seller_email is not None:
        payload["S_EMAILADDRESS"] = seller_email
    if seller_customer_number is not None:
        payload["S_CUSTOMERNUMBER"] = seller_customer_number
    if seller_role_remark is not None:
        payload["S_ROLEREMARK"] = seller_role_remark
    if original_invoice_seller_id is not None:
        payload["ORIGINALINVOICESELLERID"] = original_invoice_seller_id
    if original_invoice_buyer_id is not None:
        payload["ORIGINALINVOICEBUYERID"] = original_invoice_buyer_id
    if buyer_address is not None:
        payload["ADDRESS"] = buyer_address
    if buyer_person_in_charge is not None:
        payload["PERSONINCHARGE"] = buyer_person_in_charge
    if buyer_telephone is not None:
        payload["TELEPHONENUMBER"] = buyer_telephone
    if buyer_facsimile is not None:
        payload["FACSIMILENUMBER"] = buyer_facsimile
    if buyer_email is not None:
        payload["EMAILADDRESS"] = buyer_email
    if buyer_customer_number is not None:
        payload["CUSTOMERNUMBER"] = buyer_customer_number
    if buyer_role_remark is not None:
        payload["ROLEREMARK"] = buyer_role_remark
    return post_einvoice("B0401", payload, wrapper="Invoice")


@mcp.tool()
def void_b2b_allowance(
    allowance_number: str = Field(description="Allowance number to void."),
    allowance_date: str = Field(description="Original allowance date (YYYYMMDD)."),
    buyer_id: str = Field(description="Buyer tax ID."),
    seller_id: str = Field(description="Seller tax ID."),
    cancel_date: str = Field(description="Cancellation date (YYYYMMDD)."),
    cancel_time: str = Field(description="Cancellation time (HHmmss)."),
    cancel_reason: str = Field(description="Cancellation reason."),
    return_tax_document_number: Annotated[Optional[str], Field(description="Return/tax document number.")] = None,
    remark: Annotated[Optional[str], Field(description="Remark.")] = None,
    allowance_type: Annotated[Optional[str], Field(description="Allowance type.")] = None,
) -> dict:
    """Void (invalidate) a B2B allowance (B0501). Uses Allowance wrapper. Returns the API response."""
    payload: dict = {
        "INVOICE_CODE": "B0501",
        "ALLOWANCENUMBER": allowance_number,
        "ALLOWANCEDATE": allowance_date,
        "BUYERID": buyer_id,
        "SELLERID": seller_id,
        "CANCELDATE": cancel_date,
        "CANCELTIME": cancel_time,
        "CANCELREASON": cancel_reason,
    }
    if return_tax_document_number is not None:
        payload["RETURNTAXDOCUMENT_NUMBER"] = return_tax_document_number
    if remark is not None:
        payload["REMARK"] = remark
    if allowance_type is not None:
        payload["ALLOWANCETYPE"] = allowance_type
    return post_einvoice("B0501", payload, wrapper="Allowance")


@mcp.tool()
def create_b2b_exchange_allowance(
    allowance_number: str = Field(description="Allowance number."),
    allowance_date: str = Field(description="Allowance date (YYYYMMDD)."),
    seller_identifier: str = Field(description="Seller tax ID."),
    seller_name: str = Field(description="Seller name."),
    seller_address: str = Field(description="Seller address (mandatory)."),
    buyer_identifier: str = Field(description="Buyer tax ID."),
    buyer_name: str = Field(description="Buyer name."),
    allowance_type: str = Field(description="Allowance type."),
    items: list = Field(description="List of product items. Each item: {ALLOWANCESEQUENCENUMBER, ORIGINALINVOICEDATE, ORIGINALINVOICENUMBER, ORIGINALDESCRIPTION, QUANTITY, UNITPRICE, AMOUNT, TAX, TAXTYPE, optional: UNIT, ORIGINALSEQUENCENUMBER}."),
    tax_amount: str = Field(description="Tax amount."),
    total_amount: str = Field(description="Total amount."),
    seller_person_in_charge: Annotated[Optional[str], Field(description="Seller person in charge.")] = None,
    seller_telephone: Annotated[Optional[str], Field(description="Seller telephone number.")] = None,
    seller_facsimile: Annotated[Optional[str], Field(description="Seller facsimile number.")] = None,
    seller_email: Annotated[Optional[str], Field(description="Seller email address.")] = None,
    buyer_address: Annotated[Optional[str], Field(description="Buyer address.")] = None,
    original_invoice_seller_id: Annotated[Optional[str], Field(description="Original invoice seller ID.")] = None,
    original_invoice_buyer_id: Annotated[Optional[str], Field(description="Original invoice buyer ID.")] = None,
) -> dict:
    """Create a B2B exchange allowance (B0101). Seller address is mandatory. Returns the API response."""
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

    payload: dict = {
        "INVOICE_CODE": "B0101",
        "ALLOWANCENUMBER": allowance_number,
        "ALLOWANCEDATE": allowance_date,
        "Seller": seller,
        "Buyer": buyer,
        "ALLOWANCETYPE": allowance_type,
        "PRODUCTITEM": items,
        "TAXAMOUNT": tax_amount,
        "TOTALAMOUNT": total_amount,
    }
    if original_invoice_seller_id is not None:
        payload["ORIGINALINVOICESELLERID"] = original_invoice_seller_id
    if original_invoice_buyer_id is not None:
        payload["ORIGINALINVOICEBUYERID"] = original_invoice_buyer_id
    return post_einvoice("B0101", payload, wrapper="Invoice")
