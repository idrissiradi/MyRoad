import re
from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from passlib.context import CryptContext

from app.core.config import settings
from app.models.user import User
from app.services.user import generate_username, get_user_by_email, get_user_by_username
from app.utils.dependencies import SessionDep

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
	return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
	return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
	to_encode = data.copy()
	if expires_delta:
		expire = datetime.now(UTC) + expires_delta
	else:
		expire = datetime.now(UTC) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
	to_encode.update({"exp": expire})
	encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

	return encoded_jwt


def validate_email(session: SessionDep, email: str) -> tuple[bool, str]:
	"""Validate email format and availability"""
	email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
	if not re.match(email_regex, email):
		return False, "Invalid email format"

	if get_user_by_email(session, email):
		return False, "Email already registered"

	return True, ""


def validate_password(password: str) -> tuple[bool, str]:
	"""Validate password strength"""
	if len(password) < 8:
		return False, "Password must be at least 8 characters long"
	if not re.search(r"[A-Z]", password):
		return False, "Password must contain at least one uppercase letter"
	if not re.search(r"[a-z]", password):
		return False, "Password must contain at least one lowercase letter"
	if not re.search(r"\d", password):
		return False, "Password must contain at least one number"

	return True, ""


def validate_full_name(full_name: str) -> tuple[bool, str]:
	"""Validate full name format"""
	if not full_name or len(full_name) < 3:
		return False, "Full name must be at least 3 characters long"
	if not re.match(r"^[a-zA-Z\s]+$", full_name):
		return False, "Full name can only contain letters and spaces"

	return True, ""


def authenticate_user(session: SessionDep, email: str, password: str) -> Any | None:
	"""Authenticate user with email and password"""
	user = get_user_by_email(session, email)

	if not user:
		return None
	if not verify_password(password, user.hashed_password):
		return None
	if not user.is_active:
		return None
	return user


def create_user(
	session: SessionDep, email: str, password: str, full_name: str
) -> tuple[User | None, str]:
	"""Create a new user with validation"""

	# Validate full name
	valid_full_name, full_name_error = validate_full_name(full_name)
	if not valid_full_name:
		return None, full_name_error

	# Validate username
	username = generate_username(full_name)

	valid_username = get_user_by_username(session, username)
	if valid_username:
		return None, "Username already exists"

	# Validate email
	valid_email, email_error = validate_email(session, email)
	if not valid_email:
		return None, email_error

	# Validate password
	valid_password, password_error = validate_password(password)
	if not valid_password:
		return None, password_error

	# Create user
	hashed_password = get_password_hash(password)
	db_user = User(
		email=email.lower(),
		hashed_password=hashed_password,
		username=username,
		full_name=full_name,
	)

	try:
		session.add(db_user)
		session.commit()
		session.refresh(db_user)
		return db_user, ""
	except Exception:
		session.rollback()
		return None, "Registration failed. Please try again."
