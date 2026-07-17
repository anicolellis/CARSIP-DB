from sqlmodel import SQLModel, Session
from pydantic import ValidationError

from carsipdb.sqlmodels import *

# Creates test data in JSON form and validates using Pydantic before adding to the DB
def sqlmodel_validate_data(reset, engine) -> None:
    if reset:
        SQLModel.metadata.drop_all(engine)
        SQLModel.metadata.create_all(engine)

    timestamp = datetime.now()

    with Session(engine) as session, session.begin():
        # Sector
        s13 = {
            "name": "13",
            "modify_time": timestamp,
            "create_time": timestamp
        }
        s14 = {
            "name": "14",
            "modify_time": timestamp,
            "create_time": timestamp
        }
        s15 = {
            "name": "15",
            "modify_time": timestamp,
            "create_time": timestamp
        }
        # Location
        l13 = {
            "name": "13 LOM",
            "modify_time": timestamp,
            "create_time": timestamp
        }
        l14 = {
            "name": "14 LOM",
            "modify_time": timestamp,
            "create_time": timestamp
        }
        l15 = {
            "name": "15 LOM",
            "modify_time": timestamp,
            "create_time": timestamp
        }
        testtype = {
            "name": "Test Device",
            "modify_time": timestamp,
            "create_time": timestamp
        }
        testmem = {
            "capacity": 32,
            "speed": 5600,
            "modify_time": timestamp,
            "create_time": timestamp
        }
        testcpu = {
            "model": "Intel Xeon Gold 5415+",
            "clock_speed": 2900,
            "physical_cores": 8,
            "logical_cores": 16,
            "modify_time": timestamp,
            "create_time": timestamp
        }
        testos = {
            "name": "Microsoft Windows 11 Enterprise",
            "version": "10.0.26200.8457",
            "build": "25H2",
            "modify_time": timestamp,
            "create_time": timestamp
        }
        testdisktype = {
            "model": "Intel Raid 1 Volume",
            "capacity": 954,
            "type": "SSD",
            "modify_time": timestamp,
            "create_time": timestamp
        }
        try:
            sector_13 = Sector.model_validate(s13)
            sector_14 = Sector.model_validate(s14)
            sector_15 = Sector.model_validate(s15)
            lom_13 = Location.model_validate(l13)
            lom_14 = Location.model_validate(l14)
            lom_15 = Location.model_validate(l15)
            test_type = Type.model_validate(testtype)
            test_mem = Memory.model_validate(testmem)
            test_cpu = CPU.model_validate(testcpu)
            win11 = OS.model_validate(testos)
            test_disktype = PhysicalDiskType.model_validate(testdisktype)
        except ValidationError as e:
            print("The following data failed to validate: ")
            print(e.json())

        session.add_all([sector_13, sector_14, sector_15, lom_13, lom_14, lom_15, test_type, test_mem, test_cpu, win11, test_disktype])
        # Examples used: CARS5 and CHEMMAT-F126
        device = {
            "location_id": 1,
            "sector_id": 1,
            "type_id": 1,
            "description": "Test",
            "name": "Test",
            "make": "Test",
            "model": "Test",
            "serial_number": "Test",
            "uptime": 3,
            "last_online": timestamp,
            "status": "Test",
            "owners": "Alex",
            "modify_time": timestamp,
            "create_time": timestamp
        }
        comp = {
            "device_id": 1,
            "bios_version": "2.48.0",
            "timezone": "(UTC-06:00) Central Time (US & Canada)",
            "reboot_pending": True,
            "cpu_count": 1,
            "memory_total": 64,
            "modify_time": timestamp,
            "create_time": timestamp
        }
        dns = {
            "name": "Test",
            "ip_address": "1.2.3.4",
            "modify_time": timestamp,
            "create_time": timestamp
        }
        dhcp = {
            "device_id": 1,
            "dns_id": 1,
            "name": "Test",
            "mac_address": "00:11:22:33:44:55",
            "ip_address": "1.2.3.4",
            "modify_time": timestamp,
            "create_time": timestamp
        }
        interf = {
            "device_id": 1,
            "name": "intel Ethernet Connection (5) I219-LM",
            "mac_address": "00:11:22:33:44:55",
            "manufacturer": "Intel",
            "speed": 1000,
            "status": "Connected",
            "modify_time": timestamp,
            "create_time": timestamp
        }
        memslot = {
            "computer_id": 1,
            "memory_id": 1,
            "slot_number": 0,
            "modify_time": timestamp,
            "create_time": timestamp
        }
        disk = {
            "computer_id": 1,
            "physicaldisktype_id": 1,
            "smart_status": "OK",
            "firmware": "1.0.",
            "modify_time": timestamp,
            "create_time": timestamp
        }
        volume = {
            "physicaldisk_id": 1,
            "capacity": 952.6,
            "file_system": "NTFS",
            "usage": "17%",
            "modify_time": timestamp,
            "create_time": timestamp
        }
        try:
            test_device = Device.model_validate(device)
            test_computer = Computer.model_validate(comp)
            test_dns = DNS.model_validate(dns)
            test_dhcp = DHCP.model_validate(dhcp)
            test_interface = Interface.model_validate(interf)
            test_mem_slot = MemorySlot.model_validate(memslot)
            test_disk = PhysicalDisk.model_validate(disk)
            test_volume = Volume.model_validate(volume)
        except ValidationError as e:
            print("The following data failed to validate: ")
            print(e.json())
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

# Creates test data using SQLModel models
def sqlmodel_sample_data(reset, engine) -> None:
    if reset:
        SQLModel.metadata.drop_all(engine)
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
