"""Invoice number tools — A01, C01, Z21, Z22."""

from typing import Annotated, Optional
from pydantic import Field
from app import mcp
from connectors.einvoice_client import post_einvoice


@mcp.tool()
def get_invoice_numbers(
    tax_month: Annotated[Optional[str], Field(description="Invoice period (YYMM, e.g. '11304'). If empty, gets current period.")] = None,
    invoice_header: Annotated[Optional[str], Field(description="Invoice track (2 uppercase letters, e.g. 'DC'). If empty, auto-assigned.")] = None,
) -> dict:
    """Get invoice number allocation for the current period (A01). Returns track, start/end numbers, and QRCode AES key."""
    payload = {}
    if tax_month:
        payload["TAXMONTH"] = tax_month
    if invoice_header:
        payload["INVOICEHEADER"] = invoice_header
    return post_einvoice("A01", payload)


@mcp.tool()
def get_next_period_numbers(
    tax_month: Annotated[Optional[str], Field(description="Invoice period (YYMM). If empty, gets next period.")] = None,
    invoice_header: Annotated[Optional[str], Field(description="Invoice track (2 uppercase letters).")] = None,
) -> dict:
    """Get invoice number allocation for the next period (C01). Returns track, start/end numbers, and QRCode AES key."""
    payload = {}
    if tax_month:
        payload["TAXMONTH"] = tax_month
    if invoice_header:
        payload["INVOICEHEADER"] = invoice_header
    return post_einvoice("C01", payload)


@mcp.tool()
def get_invoice_numbers_expanded(
    tax_month: Annotated[Optional[str], Field(description="Invoice period (YYMM).")] = None,
    invoice_header: Annotated[Optional[str], Field(description="Invoice track (2 uppercase letters).")] = None,
) -> dict:
    """Get invoice numbers expanded per-invoice with AESKEY for current period (Z21). Returns INVOICEDATA array with individual invoice numbers, AESKEY, and random numbers."""
    payload = {}
    if tax_month:
        payload["TAXMONTH"] = tax_month
    if invoice_header:
        payload["INVOICEHEADER"] = invoice_header
    return post_einvoice("Z21", payload)


@mcp.tool()
def get_next_period_numbers_expanded(
    tax_month: Annotated[Optional[str], Field(description="Invoice period (YYMM).")] = None,
    invoice_header: Annotated[Optional[str], Field(description="Invoice track (2 uppercase letters).")] = None,
) -> dict:
    """Get invoice numbers expanded per-invoice with AESKEY for next period (Z22). Returns INVOICEDATA array with individual invoice numbers, AESKEY, and random numbers."""
    payload = {}
    if tax_month:
        payload["TAXMONTH"] = tax_month
    if invoice_header:
        payload["INVOICEHEADER"] = invoice_header
    return post_einvoice("Z22", payload)
