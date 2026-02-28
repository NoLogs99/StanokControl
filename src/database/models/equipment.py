from typing import Optional, List
from datetime import datetime, date
from sqlmodel import SQLModel, Field, Relationship


class EquipmentType(SQLModel, table=True):
    __tablename__ = "equipment_types"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, unique=True, index=True)
    description: Optional[str] = None

    equipment: List["Equipment"] = Relationship(back_populates="type")


class Location(SQLModel, table=True):
    __tablename__ = "locations"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, unique=True, index=True)
    description: Optional[str] = None

    equipment: List["Equipment"] = Relationship(back_populates="location")


class Equipment(SQLModel, table=True):
    __tablename__ = "equipment"

    id: Optional[int] = Field(default=None, primary_key=True)

    inventory_number: str = Field(
        max_length=100,
        unique=True,
        index=True
    )

    name: str = Field(max_length=255)

    type_id: Optional[int] = Field(
        default=None,
        foreign_key="equipment_types.id"
    )

    location_id: Optional[int] = Field(
        default=None,
        foreign_key="locations.id"
    )

    status: str = Field(default="working", max_length=50)

    last_maintenance_date: Optional[date] = None
    next_maintenance_date: Optional[date] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    type: Optional["EquipmentType"] = Relationship(back_populates="equipment")
    location: Optional["Location"] = Relationship(back_populates="equipment")

    maintenance_logs: List["MaintenanceLog"] = Relationship(back_populates="equipment")
