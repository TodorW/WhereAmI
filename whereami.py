#!/usr/bin/env python3
"""Thin wrapper so `python whereami.py` keeps working alongside `python -m whereami`."""

import sys

from whereami.cli import main

if __name__ == "__main__":
    sys.exit(main())
