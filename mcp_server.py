#!/usr/bin/env python3
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import tools.system_tools  # noqa: F401
import tools.invoice_number_tools  # noqa: F401
import tools.b2c_invoice_tools  # noqa: F401
import tools.b2b_invoice_tools  # noqa: F401
import tools.allowance_tools  # noqa: F401
import tools.cancel_tools  # noqa: F401
import tools.query_tools  # noqa: F401
import tools.admin_tools  # noqa: F401

from app import mcp


def main():
    mcp.run()


if __name__ == "__main__":
    main()
