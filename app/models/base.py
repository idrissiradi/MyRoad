import uuid
from typing import Optional

from sqlmodel import Field, SQLModel

from app.models.user import User


class Base(SQLModel, table=False):
    """Represents a user Table."""

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: Optional[str] = Field(default=None)
    updated_at: Optional[str] = Field(default=None)
