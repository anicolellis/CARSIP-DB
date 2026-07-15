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
from sqlmodel import create_engine as create_smodel_engine, SQLModel, Session

from carsipdb.utils import alchemy_sample_data
from carsipdb.sqlmodels import *

A_ENGINE = None
S_ENGINE = None
SESSION = None


def main() -> None:
    """Main entry point for `carsipdb` console script."""
    parser = ArgumentParser("CARSIP-DB CLI")

    # List of CLI arguments
    parser.add_argument("-c", "--create", action="store_true", help="Used when creating tables for the first time.")
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

    sqlmodel_sample_data(args.reset, args.create, S_ENGINE)
    #alchemy_sample_data(args.reset, args.create, A_ENGINE)


def sqlmodel_sample_data(reset, create, engine) -> None:
    if reset:
        SQLModel.metadata.drop_all(engine)
    if create or reset:
        SQLModel.metadata.create_all(engine)

    with Session(engine) as session, session.begin():
        # Sector
        sector_13 = Sector(name="13", modify_time=datetime.now(), create_time=datetime.now())
        sector_14 = Sector(name="14", modify_time=datetime.now(), create_time=datetime.now())
        sector_15 = Sector(name="15", modify_time=datetime.now(), create_time=datetime.now())
        # Location
        lom_13 = Location(name="13 LOM", modify_time=datetime.now(), create_time=datetime.now())
        lom_14 = Location(name="14 LOM", modify_time=datetime.now(), create_time=datetime.now())
        lom_15 = Location(name="15 LOM", modify_time=datetime.now(), create_time=datetime.now())
        # Type
        test_type = Type(name="Test Device", modify_time=datetime.now(), create_time=datetime.now())
        # Memory
        test_mem = Memory(capacity=32, speed=5600, modify_time=datetime.now(), create_time=datetime.now())
        # CPU
        test_cpu = CPU(
            model="Intel Xeon Gold 5415+",
            clock_speed=2900,
            physical_cores=8,
            logical_cores=16,
            modify_time=datetime.now(),
            create_time=datetime.now(),
        )
        # OS
        win11 = OS(
            name="Microsoft Windows 11 Enterprise",
            version="10.0.26200.8457",
            build="25H2",
            modify_time=datetime.now(),
            create_time=datetime.now(),
        )
        # PhysicalDiskType
        test_disktype = PhysicalDiskType(
            model="Intel Raid 1 Volume", capacity=954, type="SSD", modify_time=datetime.now(), create_time=datetime.now()
        )

        session.add_all([sector_13, sector_14, sector_15, lom_13, lom_14, lom_15, test_type, test_mem, test_cpu, win11, test_disktype])
        # Examples used: CARS5 and CHEMMAT-F126
        # Device
        test_device = Device(
            location_id=1,
            sector_id=1,
            type_id=1,
            description="Test",
            name="Test",
            make="Test",
            model="Test",
            serial_number="Test",
            uptime=3,
            last_online=datetime.now(),
            status="Test",
            owners="Alex",
            modify_time=datetime.now(),
            create_time=datetime.now(),
        )
        # Computer
        test_computer = Computer(
            device_id=1,
            bios_version="2.48.0",
            timezone="(UTC-06:00) Central Time (US & Canada)",
            reboot_pending=True,
            cpu_count=1,
            memory_total=64,
            modify_time=datetime.now(),
            create_time=datetime.now(),
        )
        # DNS
        test_dns = DNS(name="Test", ip_address="1.2.3.4", modify_time=datetime.now(), create_time=datetime.now())
        # DHCP
        test_dhcp = DHCP(
            device_id=1,
            dns_id=1,
            name="Test",
            mac_address="B0:7B:25:04:A2:B6",
            ip_address="164.54.169.126",
            modify_time=datetime.now(),
            create_time=datetime.now(),
        )
        # Interface
        test_interface = Interface(
            device_id=1,
            name="Intel Ethernet Connection (5) I219-LM",
            mac_address="B0:7B:25:04:A2:B6",
            manufacturer="Intel",
            speed=1000,
            status="Connected",
            modify_time=datetime.now(),
            create_time=datetime.now(),
        )
        # MemorySlot
        test_mem_slot = MemorySlot(computer_id=1, memory_id=1, slot_number=0, modify_time=datetime.now(), create_time=datetime.now())
        # PhysicalDisk
        test_disk = PhysicalDisk(
            computer_id=1, physical_disk_type_id=1, smart_status="OK", firmware="1.0.", modify_time=datetime.now(), create_time=datetime.now()
        )
        # Volume
        test_volume = Volume(
            physical_disk_id=1, capacity=952.6, file_system="NTFS", usage="17%", modify_time=datetime.now(), create_time=datetime.now()
        )
        """Relationships:
        One to one: Computer, Device
                    Device, DHCP
                    DHCP, DNS
        Many to one: Device, Location
                     Device, Sector
                     Device, Type
                     Interface, Device
                     MemorySlot, Computer
                     MemorySlot, Memory
                     PhysicalDisk, Computer
                     PhysicalDisk, PhysicalDiskType
                     Volume, PhysicalDisk
        Many to many: Computer, CPU
                      Computer, OS
        """
        test_computer.device = test_device
        test_device.dhcp = test_dhcp
        test_dhcp.dns = test_dns
        test_device.location = session.get(Location, 1)
        test_device.sector = session.get(Sector, 1)
        test_device.type = session.get(Type, 1)
        test_interface.device = test_device
        test_mem_slot.computer = test_computer
        test_mem_slot.memory = test_mem
        test_disk.computer = test_computer
        test_disk.physical_disk_type = test_disktype
        test_volume.physical_disk = test_disk
        test_computer.cpus = [test_cpu]
        test_computer.oses = [session.get(OS, 1)]

        session.add_all([test_device, test_computer, test_dns, test_dhcp, test_interface, test_mem_slot, test_disk, test_volume])
