import random
from typing import Optional

from pydantic import EmailStr
from sqlmodel import Session, select

from app.models.user import User


def get_user_by_email(session: Session, email: EmailStr) -> Optional[User]:
	statement = select(User).where(User.email == email)
	return session.exec(statement).first()


def get_user_by_id(session: Session, user_id: int) -> Optional[User]:
	return session.get(User, user_id)


def get_user_by_username(session: Session, username: str) -> Optional[User]:
	statement = select(User).where(User.username == username)
	return session.exec(statement).first()


def generate_username(full_name: str) -> str:
	"""Generate a username from full_name."""
	name_parts = full_name.strip().lower().split()
	first_name = name_parts[0]
	unique_number = random.randint(100, 999)
	return f"{first_name}_{unique_number}"


def update_user(session: Session, user_id: int, **kwargs) -> User:
	user = session.get(User, user_id)
	if not user:
		return None

	for key, value in kwargs.items():
		if hasattr(user, key):
			setattr(user, key, value)

	session.commit()
	session.refresh(user)
	return user
