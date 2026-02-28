from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class Role(SQLModel, table=True):
    __tablename__ = "roles"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=50, unique=True, index=True)
    description: Optional[str] = None

    users: List["User"] = Relationship(back_populates="role")
