import secrets
from typing import Literal

from fastapi.security import HTTPBearer
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
	model_config = SettingsConfigDict(
		env_file="../../.env",
		env_ignore_empty=True,
		extra="ignore",
	)

	PROJECT_NAME: str = "MyRoad"

	security: HTTPBearer = HTTPBearer()
	SECRET_KEY: str = secrets.token_urlsafe(32)
	ALGORITHM: str = "HS256"
	ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

	SQLALCHEMY_DATABASE_URI: str = "sqlite:///database.db"
	ENVIRONMENT: Literal["local", "staging", "production"] = "local"


settings = Settings()
