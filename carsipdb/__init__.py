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

from sqlalchemy import create_engine as create_alch_engine
from sqlmodel import create_engine as create_smodel_engine

from carsipdb.utils import *
from carsipdb.sqlmodels import *

A_ENGINE = None
S_ENGINE = None
SESSION = None


def main() -> None:
    """Main entry point for `carsipdb` console script."""
    parser = ArgumentParser("CARSIP-DB CLI")

    # List of CLI arguments
    parser.add_argument("-r", "--reset", action="store_true", help="Clear all previous data from the DB before running the script.")
    parser.add_argument("-u", "--username", type=str, help="Database username.")
    parser.add_argument("-p", "--password", type=str, help="Database password.")
    parser.add_argument("-H", "--hostname", type=str, help="Hostname for database.")
    parser.add_argument("-P", "--port", type=int, help="Port number for database.")
    parser.add_argument("-n", "--name", type=str, help="Database name.")
    args = parser.parse_args()

    DATABASE_URI = f"postgresql+psycopg2://{args.username}:{args.password}@{args.hostname}:{args.port}/{args.name}"

    global A_ENGINE, SESSION

    A_ENGINE = create_alch_engine(DATABASE_URI, echo=True)
    S_ENGINE = create_smodel_engine(DATABASE_URI, echo=True)

    sqlmodel_validate_data(args.reset, S_ENGINE)
    #sqlmodel_sample_data(args.reset, S_ENGINE)
    #alchemy_sample_data(args.reset, A_ENGINE)