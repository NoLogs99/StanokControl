from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship


class ActionLog(SQLModel, table=True):
    __tablename__ = "action_logs"

    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: Optional[int] = Field(
        default=None,
        foreign_key="users.id"
    )

    equipment_id: Optional[int] = Field(
        default=None,
        foreign_key="equipment.id"
    )

    action: str

    created_at: datetime = Field(default_factory=datetime.utcnow)

    user: Optional["User"] = Relationship(back_populates="action_logs")
