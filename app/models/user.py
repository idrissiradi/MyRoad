import uuid
from datetime import UTC, datetime
from typing import Optional

from sqlalchemy import text
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
	"""Represents a user Table."""

	id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
	username: str = Field(index=True, unique=True, max_length=50)
	email: str = Field(index=True, unique=True, max_length=100)
	full_name: Optional[str] = Field(default=None, max_length=100)
	is_active: bool = Field(default=True)
	is_superuser: bool = Field(default=False)
	hashed_password: str = Field(max_length=128)
	last_login: Optional[datetime] = Field(default=None)

	created_at: Optional[datetime] = Field(
		default_factory=lambda: datetime.now(UTC),
		nullable=False,
		sa_column_kwargs={"server_default": text("CURRENT_TIMESTAMP")},
	)
	updated_at: Optional[datetime] = Field(
		default_factory=lambda: datetime.now(UTC),
		nullable=False,
		sa_column_kwargs={
			"server_default": text("CURRENT_TIMESTAMP"),
			"onupdate": text("CURRENT_TIMESTAMP"),
		},
	)

	def __repr__(self):
		return f"User(id={self.id}, username={self.username}, email={self.email}, full_name={self.full_name})"

	def __str__(self):
		return f"User: {self.username} ({self.email})"


class TokenData(SQLModel, table=True):
	"""Base class for tokens."""

	id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
	user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)
	token: str = Field(unique=True, index=True)
	expires_at: datetime

	created_at: Optional[datetime] = Field(
		default_factory=lambda: datetime.now(UTC),
		nullable=False,
		sa_column_kwargs={"server_default": text("CURRENT_TIMESTAMP")},
	)
