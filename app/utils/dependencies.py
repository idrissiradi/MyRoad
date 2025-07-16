from typing import Annotated

import jwt
from fastapi import Depends, Request
from fastapi.templating import Jinja2Templates
from jwt.exceptions import InvalidTokenError
from sqlmodel import Session

from app.core.config import settings
from app.core.database import get_session
from app.models.user import User
from app.services.user import get_user_by_username

templates = Jinja2Templates(directory="app/templates")

SessionDep = Annotated[Session, Depends(get_session)]


def get_current_user(request: Request, session: SessionDep) -> User | None:
	"""Dependency to get the current user if authenticated, otherwise None"""
	try:
		token = request.cookies.get("access_token")
		if not token:
			return None

		if token.startswith("Bearer "):
			token = token[7:]

		payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

		username = payload.get("sub")
		if username is None:
			return None

		if username is None:
			return None
		user = get_user_by_username(session, username)
		return user
	except InvalidTokenError:
		return None


CurrentUser = Annotated[User, Depends(get_current_user)]
