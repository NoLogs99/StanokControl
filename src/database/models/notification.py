from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship


class Notification(SQLModel, table=True):
    __tablename__ = "notifications"

    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: int = Field(foreign_key="users.id")
    equipment_id: int = Field(foreign_key="equipment.id")

    notification_type: str = Field(max_length=50)
    message: str

    is_sent: bool = Field(default=False)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    sent_at: Optional[datetime] = None

    user: Optional["User"] = Relationship(back_populates="notifications")
