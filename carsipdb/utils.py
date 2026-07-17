#!/usr/bin/python
# ----------------------------------------------------------------------------------
# Project: CARSIP-DB
# File: carsipdb/utils.py
# ----------------------------------------------------------------------------------
# Purpose:
# This file contains utility scripts for the CARSIP-DB project.
# ----------------------------------------------------------------------------------
# Copyright (c) 2026 GSECARS, The University of Chicago, USA
# Copyright (c) 2026 NSF SEES, USA
# ----------------------------------------------------------------------------------

import datetime

from sqlalchemy.orm import Session

from carsipdb.carsip_models import (
    Base,
    Device,
    Computer,
    DHCP,
    DNS,
    Sector,
    Location,
    Type,
    Interface,
    CPU,
    Memory,
    MemorySlot,
    OS,
    PhysicalDisk,
    PhysicalDiskType,
    Volume,
)


# Creates test data for each SQLAlchemy model
def alchemy_sample_data(reset, engine) -> None:
    if reset:
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

    with Session(engine) as session, session.begin():
        # Sector
        sector_13 = Sector(name="13", modify_time=datetime.datetime.now(), create_time=datetime.datetime.now())
        sector_14 = Sector(name="14", modify_time=datetime.datetime.now(), create_time=datetime.datetime.now())
        sector_15 = Sector(name="15", modify_time=datetime.datetime.now(), create_time=datetime.datetime.now())
        # Location
        lom_13 = Location(name="13 LOM", modify_time=datetime.datetime.now(), create_time=datetime.datetime.now())
        lom_14 = Location(name="14 LOM", modify_time=datetime.datetime.now(), create_time=datetime.datetime.now())
        lom_15 = Location(name="15 LOM", modify_time=datetime.datetime.now(), create_time=datetime.datetime.now())
        # Type
        test_type = Type(name="Test Device", modify_time=datetime.datetime.now(), create_time=datetime.datetime.now())
        # Memory
        test_mem = Memory(capacity=32, speed=5600, modify_time=datetime.datetime.now(), create_time=datetime.datetime.now())
        # CPU
        test_cpu = CPU(
            model="Intel Xeon Gold 5415+",
            clock_speed=2900,
            physical_cores=8,
            logical_cores=16,
            modify_time=datetime.datetime.now(),
            create_time=datetime.datetime.now(),
        )
        # OS
        win11 = OS(
            name="Microsoft Windows 11 Enterprise",
            version="10.0.26200.8457",
            build="25H2",
            modify_time=datetime.datetime.now(),
            create_time=datetime.datetime.now(),
        )
        # PhysicalDiskType
        test_disktype = PhysicalDiskType(
            model="Intel Raid 1 Volume", capacity=954, type="SSD", modify_time=datetime.datetime.now(), create_time=datetime.datetime.now()
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
            last_online=datetime.datetime.now(),
            status="Test",
            owners="Alex",
            modify_time=datetime.datetime.now(),
            create_time=datetime.datetime.now(),
        )
        # Computer
        test_computer = Computer(
            device_id=1,
            cpu_id=1,
            bios_version="2.48.0",
            timezone="(UTC-06:00) Central Time (US & Canada)",
            reboot_pending=True,
            cpu_count=1,
            memory_total=64,
            modify_time=datetime.datetime.now(),
            create_time=datetime.datetime.now(),
        )
        # DNS
        test_dns = DNS(name="Test", ip_address="1.2.3.4", modify_time=datetime.datetime.now(), create_time=datetime.datetime.now())
        # DHCP
        test_dhcp = DHCP(
            device_id=1,
            dns_id=1,
            name="Test",
            mac_address="B0:7B:25:04:A2:B6",
            ip_address="164.54.169.126",
            modify_time=datetime.datetime.now(),
            create_time=datetime.datetime.now(),
        )
        # Interface
        test_interface = Interface(
            device_id=1,
            name="Intel Ethernet Connection (5) I219-LM",
            mac_address="B0:7B:25:04:A2:B6",
            manufacturer="Intel",
            speed=1000,
            status="Connected",
            modify_time=datetime.datetime.now(),
            create_time=datetime.datetime.now(),
        )
        # MemorySlot
        test_mem_slot = MemorySlot(computer_id=1, memory_id=1, slot_number=0, modify_time=datetime.datetime.now(), create_time=datetime.datetime.now())
        # PhysicalDisk
        test_disk = PhysicalDisk(
            computer_id=1, physical_disk_type_id=1, smart_status="OK", firmware="1.0.", modify_time=datetime.datetime.now(), create_time=datetime.datetime.now()
        )
        # Volume
        test_volume = Volume(
            physical_disk_id=1, capacity=952.6, file_system="NTFS", usage="17%", modify_time=datetime.datetime.now(), create_time=datetime.datetime.now()
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
        loc = session.get(Location, 1)
        if loc is None:
            print("Error: Test Location not found")
        else:
            test_device.location = loc
        sect = session.get(Sector, 1)
        if sect is None:
            print("Error: Test Sector not found")
        else:
            test_device.sector = sect
        typ = session.get(Type, 1)
        if typ is None:
            print("Error: Test Type not found")
        else:
            test_device.type = typ
        test_interface.device = test_device
        test_mem_slot.computer = test_computer
        test_mem_slot.memory = test_mem
        test_disk.computer = test_computer
        test_disk.physical_disk_type = test_disktype
        test_volume.physical_disk = test_disk
        test_computer.cpus = [test_cpu]
        ose = session.get(OS, 1)
        if ose is None:
            print("Error: Test OS not found")
        else:
            test_computer.oses = [ose]

        session.add_all([test_device, test_computer, test_dns, test_dhcp, test_interface, test_mem_slot, test_disk, test_volume])
