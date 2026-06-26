import datetime
from typing import List, Optional

from sqlalchemy import DateTime, Integer, String, Text, Boolean, ForeignKey, Column, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    # Can you create shared fields like this?
    modify_time: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now)
    create_time: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} - {', '.join(f'{k}: {v}' for k, v in self._columns.items())}>"

# Should we make an individual one for each Many-to-Many relationship?
association_table = Table(
    "association_table",
    Base.metadata,
    Column("left_id", ForeignKey("left_table.id"), primary_key=True),
    Column("right_id", ForeignKey("right_table.id"), primary_key=True),
)

class Device(Base):
    __tablename__ = "device"

    id: Mapped[int] = mapped_column(primary_key=True)

    location_id: Mapped[int] = mapped_column(ForeignKey("location.id")) # Many to one
    sector_id: Mapped[int] = mapped_column(ForeignKey("sector.id")) # Many to one
    type_id: Mapped[int] = mapped_column(ForeignKey("type.id")) # Many to one

    location: Mapped["Location"] = relationship(back_populates="devices")
    sector: Mapped["Sector"] = relationship(back_populates="devices")
    type: Mapped["Type"] = relationship(back_populates="devices")
    computer: Mapped[Optional["Device"]] = relationship(back_populates="device")
    dhcp: Mapped["DHCP"] = relationship(back_populates="device")
    interfaces: Mapped[List["Interface"]] = relationship(back_populates="device")

    description: Mapped[str] = mapped_column(Text)
    name: Mapped[str] = mapped_column(String(64))
    make: Mapped[str] = mapped_column(String(64))
    model: Mapped[str] = mapped_column(String(64))
    serial_number: Mapped[str] = mapped_column(String(64))
    uptime: Mapped[int] = mapped_column(Integer)
    last_online: Mapped[datetime.datetime] = mapped_column(DateTime)
    status: Mapped[str] = mapped_column(String(64))
    owners: Mapped[str] = mapped_column(String(64))

class Computer(Base):
    __tablename__ = "computer"

    id: Mapped[int] = mapped_column(primary_key=True)

    device_id: Mapped[int] = mapped_column(ForeignKey("device.id")) # One to one
    cpu_id: Mapped[int] = mapped_column(ForeignKey("cpu.id")) # Many to many

    device: Mapped["Device"] = relationship(back_populates="computer")
    cpus: Mapped[List["CPU"]] = relationship(secondary=association_table, back_populates="computers")
    memory_slots: Mapped[List["MemorySlot"]] = relationship(back_populates="computer")
    oses: Mapped[List["OS"]] = relationship(secondary=association_table, back_populates="computers")
    physical_disks: Mapped[List["PhysicalDisk"]] = relationship(back_populates="computer")

    bios_version: Mapped[str] = mapped_column(String(64))
    timezone: Mapped[str] = mapped_column(String(64))
    reboot_pending: Mapped[bool] = mapped_column(Boolean)
    cpu_count: Mapped[int] = mapped_column(Integer)
    memory_total: Mapped[int] = mapped_column(Integer)

class DHCP(Base):
    __tablename__ = "dhcp"

    id: Mapped[int] = mapped_column(primary_key=True)

    device_id: Mapped[int] = mapped_column(ForeignKey("device.id")) # One to one
    dns_id: Mapped[int] = mapped_column(ForeignKey("dns.id")) # One to one

    device: Mapped["Device"] = relationship(back_populates="dhcp")
    dns: Mapped["DNS"] = relationship(back_populates="dhcp")

    name: Mapped[str] = mapped_column(String(64))
    mac_address: Mapped[str] = mapped_column(String(64))
    ip_address: Mapped[str] = mapped_column(String(64))

class DNS(Base):
    __tablename__ = "dns"

    id: Mapped[int] = mapped_column(primary_key=True)

    dhcp: Mapped["DHCP"] = relationship(back_populates="dns")

    name: Mapped[str] = mapped_column(String(64))
    ip_address: Mapped[str] = mapped_column(String(64))

class Type(Base):
    __tablename__ = "type"

    id: Mapped[int] = mapped_column(primary_key=True)

    devices: Mapped[List["Device"]] = relationship(back_populates="type")

    name: Mapped[str] = mapped_column(String(64))

class Location(Base):
    __tablename__ = "location"

    id: Mapped[int] = mapped_column(primary_key=True)

    devices: Mapped[List["Device"]] = relationship(back_populates="location")

    name: Mapped[str] = mapped_column(String(64))

class Sector(Base):
    __tablename__ = "sector"

    id: Mapped[int] = mapped_column(primary_key=True)

    devices: Mapped[List["Device"]] = relationship(back_populates="sector")

    name: Mapped[str] = mapped_column(String(64))

class Interface(Base):
    __tablename__ = "interface"

    id: Mapped[int] = mapped_column(primary_key=True)

    device_id: Mapped[int] = mapped_column(ForeignKey("device.id")) # Many to one

    device: Mapped["Device"] = relationship(back_populates="interfaces")

    name: Mapped[str] = mapped_column(String(64))
    mac_address: Mapped[str] = mapped_column(String(64))
    manufacturer: Mapped[str] = mapped_column(String(64))
    speed: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(64))

class CPU(Base):
    __tablename__ = "cpu"

    id: Mapped[int] = mapped_column(primary_key=True)

    computers: Mapped[List["Computer"]] = relationship(secondary=association_table, back_populates="cpus")

    model: Mapped[str] = mapped_column(String(64))
    clock_speed: Mapped[int] = mapped_column(Integer)
    physical_cores: Mapped[int] = mapped_column(Integer)
    logical_cores: Mapped[int] = mapped_column(Integer)

class Memory(Base):
    __tablename__ = "memory"

    id: Mapped[int] = mapped_column(primary_key=True)

    memory_slots: Mapped[List["MemorySlot"]] = relationship(back_populates="memory")

    capacity: Mapped[int] = mapped_column(Integer)
    speed: Mapped[int] = mapped_column(Integer)

class MemorySlot(Base):
    __tablename__ = "memory_slot"

    id: Mapped[int] = mapped_column(primary_key=True)

    computer_id: Mapped[int] = mapped_column(ForeignKey("computer.id")) # Many to one
    memory_id: Mapped[int] = mapped_column(ForeignKey("memory.id")) # Many to one

    computer: Mapped["Computer"] = relationship(back_populates="memory_slots")
    memory: Mapped["Memory"] = relationship(back_populates="memory_slots")

    slot_number: Mapped[int] = mapped_column(Integer)

class OS(Base):
    __tablename__ = "os"

    id: Mapped[int] = mapped_column(primary_key=True)

    computers: Mapped[List["Computer"]] = relationship(secondary=association_table, back_populates="oses")

    name: Mapped[str] = mapped_column(String(64))
    version: Mapped[str] = mapped_column(String(64))
    build: Mapped[str] = mapped_column(String(64))

class PhysicalDisk(Base):
    __tablename__ = "physical_disk"

    id: Mapped[int] = mapped_column(primary_key=True)

    computer_id: Mapped[int] = mapped_column(ForeignKey("computer.id")) # Many to one
    physical_disk_type_id: Mapped[int] = mapped_column(ForeignKey("physical_disk_type.id")) # Many to one

    computer: Mapped["Computer"] = relationship(back_populates="physical_disks")
    physical_disk_type: Mapped["PhysicalDiskType"] = relationship(back_populates="physical_disks")
    volumes: Mapped[List["Volume"]] = relationship(back_populates="physical_disk")

    smart_status: Mapped[str] = mapped_column(String(64))
    firmware: Mapped[str] = mapped_column(String(64))

class PhysicalDiskType(Base):
    __tablename__ = "physical_disk_type"

    id: Mapped[int] = mapped_column(primary_key=True)

    physical_disks: Mapped[List[PhysicalDisk]] = relationship(back_populates="physical_disk_type")

    model: Mapped[str] = mapped_column(String(64))
    capacity: Mapped[int] = mapped_column(Integer)
    type: Mapped[str] = mapped_column(String(64))

class Volume(Base):
    __tablename__ = "volume"

    id: Mapped[int] = mapped_column(primary_key=True)

    physical_disk_id: Mapped[int] = mapped_column(ForeignKey("physical_disk.id")) # Many to one

    physical_disk: Mapped["PhysicalDisk"] = relationship(back_populates="volumes")

    capacity: Mapped[int] = mapped_column(Integer)
    file_system: Mapped[str] = mapped_column(String(64))
    usage: Mapped[str] = mapped_column(String(64))