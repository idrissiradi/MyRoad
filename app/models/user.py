from sqlmodel import Field, SQLModel
from typing import Optional
import uuid


class User(SQLModel, table=True):
    """Represents a user Table."""

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    username: str = Field(index=True, unique=True, max_length=50)
    email: str = Field(index=True, unique=True, max_length=100)
    full_name: Optional[str] = Field(default=None, max_length=100)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    hashed_password: str = Field(max_length=128)
    created_at: Optional[str] = Field(default=None)
    updated_at: Optional[str] = Field(default=None)
    last_login: Optional[str] = Field(default=None)

    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, email={self.email}, full_name={self.full_name})"

    def __str__(self):
        return f"User: {self.username} ({self.email})"
