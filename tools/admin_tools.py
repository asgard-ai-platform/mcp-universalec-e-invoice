"""Admin tools — Z32, E0401, E0402."""

from typing import Annotated, Optional
from pydantic import Field
from app import mcp
from connectors.einvoice_client import post_einvoice


@mcp.tool()
def upload_next_period_tracks(
    head_ban: str = Field(description="Head company tax ID (HeadBan)."),
    branch_ban: str = Field(description="Branch company tax ID (BranchBan)."),
    invoice_type: str = Field(description="Invoice type code."),
    year_month: str = Field(description="Year-month period (YYMM format) for next period."),
    invoice_track: str = Field(description="Invoice track (2 uppercase letters)."),
    invoice_begin_no: str = Field(description="Beginning invoice number for the track."),
    invoice_end_no: str = Field(description="Ending invoice number for the track."),
) -> dict:
    """Upload next period invoice track allocation data (Z32). Returns the API response."""
    payload = {
        "INVOICE_CODE": "Z32",
        "HeadBan": head_ban,
        "BranchBan": branch_ban,
        "InvoiceType": invoice_type,
        "YearMonth": year_month,
        "InvoiceTrack": invoice_track,
        "InvoiceBeginNo": invoice_begin_no,
        "InvoiceEndNo": invoice_end_no,
    }
    return post_einvoice("Z32", payload, wrapper="Invoice")


@mcp.tool()
def assign_branch_tracks(
    head_ban: str = Field(description="Head company tax ID (HeadBan)."),
    branch_ban: str = Field(description="Branch company tax ID (BranchBan)."),
    invoice_type: str = Field(description="Invoice type code."),
    year_month: str = Field(description="Year-month period (YYMM format)."),
    invoice_track: str = Field(description="Invoice track (2 uppercase letters)."),
    invoice_begin_no: str = Field(description="Beginning invoice number for the main track."),
    invoice_end_no: str = Field(description="Ending invoice number for the main track."),
    branch_track_items: list = Field(description="List of branch track items. Each item: {InvoiceBeginNo, InvoiceEndNo, InvoiceBooklet}."),
) -> dict:
    """Assign invoice track ranges to a branch (E0401). Returns the API response."""
    payload = {
        "INVOICE_CODE": "E0401",
        "Main": {
            "HeadBan": head_ban,
            "BranchBan": branch_ban,
            "InvoiceType": invoice_type,
            "YearMonth": year_month,
            "InvoiceTrack": invoice_track,
            "InvoiceBeginNo": invoice_begin_no,
            "InvoiceEndNo": invoice_end_no,
        },
        "Details": {
            "BranchTrackItem": branch_track_items,
        },
    }
    return post_einvoice("E0401", payload, wrapper="Invoice")


@mcp.tool()
def report_unused_tracks(
    head_ban: str = Field(description="Head company tax ID (HeadBan)."),
    branch_ban: str = Field(description="Branch company tax ID (BranchBan)."),
    invoice_type: str = Field(description="Invoice type code."),
    year_month: str = Field(description="Year-month period (YYMM format)."),
    invoice_track: str = Field(description="Invoice track (2 uppercase letters)."),
    blank_items: list = Field(description="List of unused (blank) track ranges. Each item: {InvoiceBeginNo, InvoiceEndNo}."),
) -> dict:
    """Report unused invoice track ranges back to the system (E0402). Returns the API response."""
    payload = {
        "INVOICE_CODE": "E0402",
        "Main": {
            "HeadBan": head_ban,
            "BranchBan": branch_ban,
            "InvoiceType": invoice_type,
            "YearMonth": year_month,
            "InvoiceTrack": invoice_track,
        },
        "Details": {
            "BranchTrackBlankItem": blank_items,
        },
    }
    return post_einvoice("E0402", payload, wrapper="Invoice")
