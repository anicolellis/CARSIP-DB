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

import datetime
from argparse import ArgumentParser

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from carsipdb.carsip_models import *

ENGINE = None
SESSION = None

def main() -> None:
    """Main entry point for `carsipdb` console script."""
    parser = ArgumentParser("CARSIP-DB CLI")

    # List of CLI arguments
    parser.add_argument("-c", "--create", action="store_true", help="Whether new tables need to be created.")
    parser.add_argument("-e", "--enum", action="store_true", help="Whether enum data needs to be added.")
    parser.add_argument("-r", "--reset", action="store_true", help="Clear all previous data from the DB.")
    args = parser.parse_args()

    DATABASE_URI="postgresql+psycopg2://nicolellis:atti3WbEAzyjN87WMhBX@localhost:5432/carsip"

    global ENGINE, SESSION

    ENGINE = create_engine(DATABASE_URI, echo=True)

    if args.reset:
        Base.metadata.drop_all(ENGINE)
        Base.metadata.create_all(ENGINE)
    elif args.create:
        Base.metadata.create_all(ENGINE)
    
    # Test connecting via relationships in both directions for all types
    with Session(ENGINE) as session, session.begin():

        if args.enum:
            #Type, Location, Sector, Memory, CPU, OS, PhysicalDiskType
            #Sector
            sector_13 = Sector(name="13",
                            modify_time=datetime.datetime.now(),
                            create_time=datetime.datetime.now())
            sector_14 = Sector(name="14",
                            modify_time=datetime.datetime.now(),
                            create_time=datetime.datetime.now())
            sector_15 = Sector(name="15",
                            modify_time=datetime.datetime.now(),
                            create_time=datetime.datetime.now())
            #Location
            lom_13 = Location(name="13 LOM",
                            modify_time=datetime.datetime.now(),
                            create_time=datetime.datetime.now())
            lom_14 = Location(name="14 LOM",
                            modify_time=datetime.datetime.now(),
                            create_time=datetime.datetime.now())
            lom_15 = Location(name="15 LOM",
                            modify_time=datetime.datetime.now(),
                            create_time=datetime.datetime.now())
            
            #Type
            test_type = Type(name="Test Device",
                            modify_time=datetime.datetime.now(),
                            create_time=datetime.datetime.now())
            
            session.add_all([sector_13, sector_14, sector_15, lom_13, lom_14, lom_15, test_type])
        
        test_device = Device(location_id=1,
                             sector_id=1,
                             type_id=1,
                             description="Test",
                             name="Test",
                             make="Test",
                             model="Test",
                             serial_number="Test",
                             uptime=3,
                             last_online=datetime.datetime.now(),
                             status="Test",
                             owners="Alex",
                             modify_time=datetime.datetime.now(),
                             create_time=datetime.datetime.now())
        session.add(test_device)
