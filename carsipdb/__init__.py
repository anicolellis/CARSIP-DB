#!/usr/bin/python
# ----------------------------------------------------------------------------------
# Project: CARSIP-DB
# File: carsipdb/__init__.py
# ----------------------------------------------------------------------------------
# Purpose:
# This file is used to initialize the carsipdb package.
# ----------------------------------------------------------------------------------
# Copyright (c) 2026 GSECARS, The University of Chicago, USA
# Copyright (c) 2026 NSF SEES, USA
# ----------------------------------------------------------------------------------

from argparse import ArgumentParser


def main() -> None:
    """Main entry point for `carsipdb` console script."""
    parser = ArgumentParser("CARSIP-DB CLI")

    # List of CLI arguments

    args = parser.parse_args()

    parser.print_help()
