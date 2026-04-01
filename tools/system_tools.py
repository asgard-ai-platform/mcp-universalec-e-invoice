"""System tools — Y01 get system time / connection test."""

from app import mcp
from connectors.einvoice_client import post_einvoice


@mcp.tool()
def get_system_time() -> dict:
    """Get the e-invoice server system time. Also serves as a connection test (Y01)."""
    return post_einvoice("Y01", {})
