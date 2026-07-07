from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship

class Base(SQLModel, table=False):
    modify_time: datetime
    create_time: datetime

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
    
    location: "Location" | None = Relationship(back_populates="devices")
    sector: "Sector" | None = Relationship(back_populates="devices")
    type: "Type" | None = Relationship(back_populates="devices")
    computer: "Computer" | None = Relationship(back_populates="device")
    dhcp: "DHCP" | None = Relationship(back_populates="device")
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
    id:int | None = Field(default=None, primary_key=True)

    name: str
    mac_address: str
    ip_address: str

    device_id: int | None = Field(default=None, foreign_key="device.id")
    dns_id: int | None = Field(default=None, foreign_key="dns.id")

    device: Device = Relationship(back_populates="dhcp")
    dns: "DNS" = Relationship(back_populates="dhcp")
