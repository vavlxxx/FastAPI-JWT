from datetime import timedelta
from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    UVICORN_PORT: int = 8000
    UVICORN_HOST: str = "127.0.0.1"
    UVICORN_RELOAD: bool = True

    JWT_EXPIRE_DELTA_ACCESS: timedelta = timedelta(minutes=5)
    JWT_EXPIRE_DELTA_REFRESH: timedelta = timedelta(days=7)
    JWT_ALGORITHM: str = "RS256"
    JWT_PRIVATE_KEY: Path = BASE_DIR / "creds/jwt-private.pem"
    JWT_PUBLIC_KEY: Path = BASE_DIR / "creds/jwt-public.pem"


settings = Settings()
