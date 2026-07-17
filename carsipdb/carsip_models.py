import datetime
from dataclasses import dataclass, field
from typing import List, Optional

from sqlalchemy import DateTime, Integer, String, Text, Boolean, ForeignKey, Column, Table, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    modify_time: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now)
    create_time: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now)

    _columns: dict[str, any] = field(default_factory=dict)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} - {', '.join(f'{k}: {v}' for k, v in self._columns.items())}>"


# Do the association tables need the modify and create times, or is it ok to just have them for the objects they reference?
computer_os_association_table = Table(
    "computer_os_association_table",
    Base.metadata,
    Column("computer_id", ForeignKey("computer.id"), primary_key=True),
    Column("os_id", ForeignKey("os.id"), primary_key=True),
)

computer_cpu_association_table = Table(
    "computer_cpu_association_table",
    Base.metadata,
    Column("computer", ForeignKey("computer.id"), primary_key=True),
    Column("cpu_id", ForeignKey("cpu.id"), primary_key=True),
)


@dataclass
class Device(Base):
    __tablename__ = "device"

    id: Mapped[int] = mapped_column(primary_key=True)

    location_id: Mapped[int] = mapped_column(ForeignKey("location.id"))  # Many to one
    sector_id: Mapped[int] = mapped_column(ForeignKey("sector.id"))  # Many to one
    type_id: Mapped[int] = mapped_column(ForeignKey("type.id"))  # Many to one

    location: Mapped["Location"] = relationship(back_populates="devices")
    sector: Mapped["Sector"] = relationship(back_populates="devices")
    type: Mapped["Type"] = relationship(back_populates="devices")
    computer: Mapped[Optional["Computer"]] = relationship(back_populates="device")
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

    def __post_init__(self) -> None:
        self._columns = {
            "id": self.id,
            "location_id": self.location_id,
            "sector_id": self.sector_id,
            "type_id": self.type_id,
            "description": self.description,
            "name": self.name,
            "make": self.make,
            "model": self.model,
            "serial_number": self.serial_number,
            "uptime": self.uptime,
            "last_online": self.last_online,
            "status": self.status,
            "owners": self.owners,
            "modify_time": self.modify_time,
            "create_time": self.create_time,
        }


@dataclass
class Computer(Base):
    __tablename__ = "computer"

    id: Mapped[int] = mapped_column(primary_key=True)

    device_id: Mapped[int] = mapped_column(ForeignKey("device.id"))  # One to one
    cpu_id: Mapped[int] = mapped_column(ForeignKey("cpu.id"))  # Many to many

    device: Mapped["Device"] = relationship(back_populates="computer")
    cpus: Mapped[List["CPU"]] = relationship(secondary=computer_cpu_association_table, back_populates="computers")
    memory_slots: Mapped[List["MemorySlot"]] = relationship(back_populates="computer")
    oses: Mapped[List["OS"]] = relationship(secondary=computer_os_association_table, back_populates="computers")
    physical_disks: Mapped[List["PhysicalDisk"]] = relationship(back_populates="computer")

    bios_version: Mapped[str] = mapped_column(String(64))
    timezone: Mapped[str] = mapped_column(String(64))
    reboot_pending: Mapped[bool] = mapped_column(Boolean)
    cpu_count: Mapped[int] = mapped_column(Integer)
    memory_total: Mapped[int] = mapped_column(Integer)

    def __post_init__(self) -> None:
        self._columns = {
            "id": self.id,
            "device_id": self.device_id,
            "cpu_id": self.cpu_id,
            "bios_version": self.bios_version,
            "timezone": self.timezone,
            "reboot_pending": self.reboot_pending,
            "cpu_count": self.cpu_count,
            "memory_total": self.memory_total,
            "modify_time": self.modify_time,
            "create_time": self.create_time,
        }


@dataclass
class DHCP(Base):
    __tablename__ = "dhcp"

    id: Mapped[int] = mapped_column(primary_key=True)

    device_id: Mapped[int] = mapped_column(ForeignKey("device.id"))  # One to one
    dns_id: Mapped[int] = mapped_column(ForeignKey("dns.id"))  # One to one

    device: Mapped["Device"] = relationship(back_populates="dhcp")
    dns: Mapped["DNS"] = relationship(back_populates="dhcp")

    name: Mapped[str] = mapped_column(String(64))
    mac_address: Mapped[str] = mapped_column(String(64))
    ip_address: Mapped[str] = mapped_column(String(64))

    def __post_init__(self) -> None:
        self._columns = {
            "id": self.id,
            "device_id": self.device_id,
            "dns_id": self.dns_id,
            "name": self.name,
            "mac_address": self.mac_address,
            "ip_address": self.ip_address,
            "modify_time": self.modify_time,
            "create_time": self.create_time,
        }


@dataclass
class DNS(Base):
    __tablename__ = "dns"

    id: Mapped[int] = mapped_column(primary_key=True)

    dhcp: Mapped["DHCP"] = relationship(back_populates="dns")

    name: Mapped[str] = mapped_column(String(64))
    ip_address: Mapped[str] = mapped_column(String(64))

    def __post_init__(self) -> None:
        self._columns = {
            "id": self.id,
            "name": self.name,
            "ip_address": self.ip_address,
            "modify_time": self.modify_time,
            "create_time": self.create_time,
        }


@dataclass
class Type(Base):
    __tablename__ = "type"

    id: Mapped[int] = mapped_column(primary_key=True)

    devices: Mapped[List["Device"]] = relationship(back_populates="type")

    name: Mapped[str] = mapped_column(String(64))

    def __post_init__(self) -> None:
        self._columns = {
            "id": self.id,
            "name": self.name,
            "modify_time": self.modify_time,
            "create_time": self.create_time,
        }


@dataclass
class Location(Base):
    __tablename__ = "location"

    id: Mapped[int] = mapped_column(primary_key=True)

    devices: Mapped[List["Device"]] = relationship(back_populates="location")

    name: Mapped[str] = mapped_column(String(64))

    def __post_init__(self) -> None:
        self._columns = {
            "id": self.id,
            "name": self.name,
            "modify_time": self.modify_time,
            "create_time": self.create_time,
        }


@dataclass
class Sector(Base):
    __tablename__ = "sector"

    id: Mapped[int] = mapped_column(primary_key=True)

    devices: Mapped[List["Device"]] = relationship(back_populates="sector")

    name: Mapped[str] = mapped_column(String(64))

    def __post_init__(self) -> None:
        self._columns = {
            "id": self.id,
            "name": self.name,
            "modify_time": self.modify_time,
            "create_time": self.create_time,
        }


@dataclass
class Interface(Base):
    __tablename__ = "interface"

    id: Mapped[int] = mapped_column(primary_key=True)

    device_id: Mapped[int] = mapped_column(ForeignKey("device.id"))  # Many to one

    device: Mapped["Device"] = relationship(back_populates="interfaces")

    name: Mapped[str] = mapped_column(String(64))
    mac_address: Mapped[str] = mapped_column(String(64))
    manufacturer: Mapped[str] = mapped_column(String(64))
    speed: Mapped[int] = mapped_column(Integer)  # Mbps
    status: Mapped[str] = mapped_column(String(64))

    def __post_init__(self) -> None:
        self._columns = {
            "id": self.id,
            "device_id": self.device_id,
            "name": self.name,
            "mac_address": self.mac_address,
            "manufacturer": self.manufacturer,
            "speed": self.speed,
            "status": self.status,
            "modify_time": self.modify_time,
            "create_time": self.create_time,
        }


@dataclass
class CPU(Base):
    __tablename__ = "cpu"

    id: Mapped[int] = mapped_column(primary_key=True)

    computers: Mapped[List["Computer"]] = relationship(secondary=computer_cpu_association_table, back_populates="cpus")

    model: Mapped[str] = mapped_column(String(64))
    clock_speed: Mapped[int] = mapped_column(Integer)  # MHz
    physical_cores: Mapped[int] = mapped_column(Integer)
    logical_cores: Mapped[int] = mapped_column(Integer)

    def __post_init__(self) -> None:
        self._columns = {
            "id": self.id,
            "model": self.model,
            "clock_speed": self.clock_speed,
            "physical_cores": self.physical_cores,
            "logical_cores": self.logical_cores,
            "modify_time": self.modify_time,
            "create_time": self.create_time,
        }


@dataclass
class Memory(Base):
    __tablename__ = "memory"

    id: Mapped[int] = mapped_column(primary_key=True)

    memory_slots: Mapped[List["MemorySlot"]] = relationship(back_populates="memory")

    capacity: Mapped[int] = mapped_column(Integer)
    speed: Mapped[int] = mapped_column(Integer)  # MHz

    def __post_init__(self) -> None:
        self._columns = {
            "id": self.id,
            "capacity": self.capacity,
            "speed": self.speed,
            "modify_time": self.modify_time,
            "create_time": self.create_time,
        }


@dataclass
class MemorySlot(Base):
    __tablename__ = "memory_slot"

    id: Mapped[int] = mapped_column(primary_key=True)

    computer_id: Mapped[int] = mapped_column(ForeignKey("computer.id"))  # Many to one
    memory_id: Mapped[int] = mapped_column(ForeignKey("memory.id"))  # Many to one

    computer: Mapped["Computer"] = relationship(back_populates="memory_slots")
    memory: Mapped["Memory"] = relationship(back_populates="memory_slots")

    slot_number: Mapped[int] = mapped_column(Integer)

    def __post_init__(self) -> None:
        self._columns = {
            "id": self.id,
            "computer_id": self.computer_id,
            "memory_id": self.memory_id,
            "slot_number": self.slot_number,
            "modify_time": self.modify_time,
            "create_time": self.create_time,
        }


@dataclass
class OS(Base):
    __tablename__ = "os"

    id: Mapped[int] = mapped_column(primary_key=True)

    computers: Mapped[List["Computer"]] = relationship(secondary=computer_os_association_table, back_populates="oses")

    name: Mapped[str] = mapped_column(String(64))
    version: Mapped[str] = mapped_column(String(64))
    build: Mapped[str] = mapped_column(String(64))

    def __post_init__(self) -> None:
        self._columns = {
            "id": self.id,
            "name": self.name,
            "version": self.version,
            "build": self.build,
            "modify_time": self.modify_time,
            "create_time": self.create_time,
        }


@dataclass
class PhysicalDisk(Base):
    __tablename__ = "physical_disk"

    id: Mapped[int] = mapped_column(primary_key=True)

    computer_id: Mapped[int] = mapped_column(ForeignKey("computer.id"))  # Many to one
    physical_disk_type_id: Mapped[int] = mapped_column(ForeignKey("physical_disk_type.id"))  # Many to one

    computer: Mapped["Computer"] = relationship(back_populates="physical_disks")
    physical_disk_type: Mapped["PhysicalDiskType"] = relationship(back_populates="physical_disks")
    volumes: Mapped[List["Volume"]] = relationship(back_populates="physical_disk")

    smart_status: Mapped[str] = mapped_column(String(64))
    firmware: Mapped[str] = mapped_column(String(64))

    def __post_init__(self) -> None:
        self._columns = {
            "id": self.id,
            "computer_id": self.computer_id,
            "physical_disk_type_id": self.physical_disk_type_id,
            "smart_status": self.smart_status,
            "firmware": self.firmware,
            "modify_time": self.modify_time,
            "create_time": self.create_time,
        }


class PhysicalDiskType(Base):
    __tablename__ = "physical_disk_type"

    id: Mapped[int] = mapped_column(primary_key=True)

    physical_disks: Mapped[List[PhysicalDisk]] = relationship(back_populates="physical_disk_type")

    model: Mapped[str] = mapped_column(String(64))
    capacity: Mapped[int] = mapped_column(Integer)
    type: Mapped[str] = mapped_column(String(64))

    def __post_init__(self) -> None:
        self._columns = {
            "id": self.id,
            "model": self.model,
            "capacity": self.capacity,
            "type": self.type,
            "modify_time": self.modify_time,
            "create_time": self.create_time,
        }


@dataclass
class Volume(Base):
    __tablename__ = "volume"

    id: Mapped[int] = mapped_column(primary_key=True)

    physical_disk_id: Mapped[int] = mapped_column(ForeignKey("physical_disk.id"))  # Many to one

    physical_disk: Mapped["PhysicalDisk"] = relationship(back_populates="volumes")

    capacity: Mapped[float] = mapped_column(Float)
    file_system: Mapped[str] = mapped_column(String(64))
    usage: Mapped[str] = mapped_column(String(64))  # How do we want to represent this - percentage or number of GB used

    def __post_init__(self) -> None:
        self._columns = {
            "id": self.id,
            "physical_disk_id": self.physical_disk_id,
            "capacity": self.capacity,
            "file_system": self.file_system,
            "usage": self.usage,
            "modify_time": self.modify_time,
            "create_time": self.create_time,
        }
