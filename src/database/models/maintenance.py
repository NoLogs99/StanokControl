from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship


class MaintenanceLog(SQLModel, table=True):
    __tablename__ = "maintenance_logs"

    id: Optional[int] = Field(default=None, primary_key=True)

    equipment_id: int = Field(
        foreign_key="equipment.id"
    )

    user_id: Optional[int] = Field(
        default=None,
        foreign_key="users.id"
    )

    action_type: str = Field(max_length=50)  # maintenance / repair
    description: Optional[str] = None

    action_date: datetime = Field(default_factory=datetime.utcnow)

    equipment: "Equipment" = Relationship(back_populates="maintenance_logs")
    user: Optional["User"] = Relationship(back_populates="maintenance_logs")
