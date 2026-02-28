from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str = Field(max_length=255)

    telegram_id: Optional[int] = Field(
        default=None,
        unique=True,
        index=True
    )

    role_id: Optional[int] = Field(
        default=None,
        foreign_key="roles.id"
    )

    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    role: Optional["Role"] = Relationship(back_populates="users")
    maintenance_logs: List["MaintenanceLog"] = Relationship(back_populates="user")
    action_logs: List["ActionLog"] = Relationship(back_populates="user")
    notifications: List["Notification"] = Relationship(back_populates="user")
