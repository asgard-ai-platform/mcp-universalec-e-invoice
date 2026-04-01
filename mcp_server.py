#!/usr/bin/env python3
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Tool module imports will be added as they are created.

from app import mcp


def main():
    mcp.run()


if __name__ == "__main__":
    main()
