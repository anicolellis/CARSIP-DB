from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship

class Base(SQLModel, table=False):
    modify_time: datetime
    create_time: datetime

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} - {', '.join(f'{k}: {getattr(self, k)}' for k in self.model_fields)}>"

class ComputerCPULink(SQLModel, table=True):
    computer_id: int | None = Field(default=None, foreign_key="computer.id", primary_key=True)
    cpu_id: int | None = Field(default=None, foreign_key="cpu.id", primary_key=True)

class ComputerOSLink(SQLModel, table=True):
    computer_id: int | None = Field(default=None, foreign_key="computer.id", primary_key=True)
    os_id: int | None = Field(default=None, foreign_key="os.id", primary_key=True)

class Device(Base, table=True):
    id: int | None = Field(default=None, primary_key=True)

    description: str
    name: str
    make: str
    model: str
    serial_number: str
    uptime: int
    last_online: datetime
    status: str
    owners: str 

    location_id: int | None = Field(default=None, foreign_key="location.id")
    sector_id: int | None = Field(default=None, foreign_key="sector.id")
    type_id: int | None = Field(default=None, foreign_key="type.id")
    
    location: "Location" = Relationship(back_populates="devices")
    sector: "Sector" = Relationship(back_populates="devices")
    type: "Type" = Relationship(back_populates="devices")
    computer: "Computer" | None = Relationship(back_populates="device")
    dhcp: "DHCP" = Relationship(back_populates="device")
    interfaces: list["Interface"] = Relationship(back_populates="device")

class Computer(Base, table=True):
    id: int | None = Field(default=None, primary_key=True)

    bios_version: str
    timezone: str
    reboot_pending: bool
    cpu_count: int
    memory_total: int

    device_id: int | None = Field(default=None, foreign_key="device.id")
    
    device: Device = Relationship(back_populates="computer")
    cpus: list["CPU"] = Relationship(back_populates="computers", link_model=ComputerCPULink)
    memory_slots: list["MemorySlot"] = Relationship(back_populates="computer")
    oses: list["OS"] = Relationship(back_populates="computers", link_model=ComputerOSLink)
    physical_disks: list["PhysicalDisk"] = Relationship(back_populates="computer")

class DHCP(Base, table=True):
    id: int | None = Field(default=None, primary_key=True)

    name: str
    mac_address: str
    ip_address: str

    device_id: int | None = Field(default=None, foreign_key="device.id")
    dns_id: int | None = Field(default=None, foreign_key="dns.id")

    device: Device = Relationship(back_populates="dhcp")
    dns: "DNS" = Relationship(back_populates="dhcp")

class DNS(Base, table=True):
    id: int | None = Field(default=None, primary_key=True)

    name: str
    ip_address: str

    dhcp: DHCP = Relationship(back_populates="dns")

class Type(Base, table=True):
    id: int | None = Field(default=None, primary_key=True)

    name: str

    devices: list[Device] = Relationship(back_populates="type")

class Location(Base, table=True):
    id: int | None = Field(default=None, primary_key=True)

    name: str

    devices: list[Device] = Relationship(back_populates="location")

class Sector(Base, table=True):
    id: int | None = Field(default=None, primary_key=True)

    name: str

    devices: list[Device] = Relationship(back_populates="sector")

class Interface(Base, table=True):
    id: int | None = Field(default=None, primary_key=True)

    name: str
    mac_address: str
    manufacturer: str
    speed: int
    status: str

    device_id: int | None = Field(default=None, foreign_key="device.id")

    device: Device = Relationship(back_populates="interfaces")

class CPU(Base, table=True):
    id: int | None = Field(default=None, primary_key=True)

    model: str
    clock_speed: int
    physical_cores: int
    logical_cores: int

    computers: list[Computer] = Relationship(back_populates="cpus", link_model=ComputerCPULink)

class Memory(Base, table=True):
    id: int | None = Field(default=None, primary_key=True)

    capacity: int
    speed: int

    memory_slots: list["MemorySlot"] = Relationship(back_populates="memory")

class MemorySlot(Base, table=True):
    id: int | None = Field(default=None, primary_key=True)

    slot_number: int

    computer_id: int | None = Field(default=None, foreign_key="computer.id")
    memory_id: int | None = Field(default=None, foreign_key="memory.id")

    computer: Computer = Relationship(back_populates="memory_slots")
    memory: Memory = Relationship(back_populates="memory_slots")

class OS(Base, table=True):
    id: int | None = Field(default=None, primary_key=True)

    name: str
    version: str
    build: str

    computers: list[Computer] = Relationship(back_populates="oses", link_model=ComputerOSLink)

class PhysicalDisk(Base, table=True):
    id: int | None = Field(default=None, primary_key=True)

    smart_status: str
    firmware: str

    computer_id: int | None = Field(default=None, foreign_key="computer.id")
    physical_disk_type_id: int | None = Field(default=None, foreign_key="physical_disk_type.id")

    computer: Computer = Relationship(back_populates="physical_disks")
    physical_disk_type: "PhysicalDiskType" = Relationship(back_populates="physical_disks")
    volumes: "Volume" = Relationship(back_populates="physical_disk")

class PhysicalDiskType(Base, table=True):
    id: int | None = Field(default=None, primary_key=True)

    model: str
    capacity: int
    type: str

    physical_disks: list[PhysicalDisk] = Relationship(back_populates="physical_disk_type")

class Volume(Base, table=True):
    id: int | None = Field(default=None, primary_key=True)

    capacity: int
    file_system: str
    usage: str

    physical_disk_id: int | None = Field(default=None, foreign_key="physical_disk.id")

    physical_disk: PhysicalDisk = Relationship(back_populates="volumes")