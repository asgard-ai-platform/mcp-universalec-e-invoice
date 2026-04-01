"""Query tools — Z11, Z31, Z33, Z34."""

from typing import Annotated, Optional
from pydantic import Field
from app import mcp
from connectors.einvoice_client import post_einvoice


@mcp.tool()
def get_cancel_status(
    invoice_number: str = Field(description="Invoice number to check cancellation status."),
    invoice_date: str = Field(description="Invoice date (YYYYMMDD)."),
) -> dict:
    """Get the cancellation status of an invoice (Z11). STATUSCODE: 1=completed, 2=pending, 3=failed. Returns the API response."""
    payload = {
        "INVOICE_NUMBER": invoice_number,
        "INVOICE_DATE": invoice_date,
        "REMARK": "",
    }
    return post_einvoice("Z11", payload, wrapper="INDEX")


@mcp.tool()
def get_downloaded_track_ranges(
    head_ban: str = Field(description="Head company tax ID (HeadBan)."),
    branch_ban: str = Field(description="Branch company tax ID (BranchBan)."),
    invoice_type: str = Field(description="Invoice type code."),
    year_month: str = Field(description="Year-month period (YYMM format, e.g. '11304')."),
    invoice_track: str = Field(description="Invoice track (2 uppercase letters)."),
) -> dict:
    """Get downloaded track ranges for an invoice period (Z31). Returns the API response."""
    payload = {
        "INVOICE_CODE": "Z31",
        "Main": {
            "HeadBan": head_ban,
            "BranchBan": branch_ban,
            "InvoiceType": invoice_type,
            "YearMonth": year_month,
            "InvoiceTrack": invoice_track,
        },
    }
    return post_einvoice("Z31", payload, wrapper="Invoice")


@mcp.tool()
def get_assignment_info(
    head_ban: str = Field(description="Head company tax ID (HeadBan)."),
    branch_ban: str = Field(description="Branch company tax ID (BranchBan)."),
    year_month: str = Field(description="Year-month period (YYMM format)."),
    invoice_type: str = Field(description="Invoice type code."),
) -> dict:
    """Get invoice assignment info for a period (Z33). Returns the API response."""
    payload = {
        "INVOICE_CODE": "Z33",
        "Main": {
            "HeadBan": head_ban,
            "BranchBan": branch_ban,
            "YearMonth": year_month,
            "InvoiceType": invoice_type,
        },
    }
    return post_einvoice("Z33", payload, wrapper="Invoice")


@mcp.tool()
def get_winning_list(
    year_month: str = Field(description="Year-month period (YYMM format) for the winning number list."),
) -> dict:
    """Download the winning invoice number list for a period (Z34). Returns the API response."""
    payload = {
        "INVOICE_CODE": "Z34",
        "YearMonth": year_month,
    }
    return post_einvoice("Z34", payload, wrapper="Invoice")
