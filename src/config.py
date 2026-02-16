from datetime import timedelta
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL

BASE_DIR = Path(__file__).parent.parent


class DBConfig(BaseModel):
    ### sqlalchemy
    echo: bool = False
    expire_on_commit: bool = False
    autoflush: bool = False
    autocommit: bool = False
    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

    ### database config
    host: str
    user: str
    name: str
    port: int
    password: SecretStr
    name_test: str = "jwt_db"

    @property
    def async_url(self) -> URL:
        return URL.create(
            drivername="postgresql+asyncpg",
            host=self.host,
            port=self.port,
            database=self.name,
            username=self.user,
            password=self.password.get_secret_value(),
        )


class TokenConfig(BaseModel):
    REFRESH_TOKEN_COOKIE_KEY: str = "refresh_token"
    JWT_EXPIRE_DELTA_ACCESS: timedelta = timedelta(minutes=15)
    JWT_EXPIRE_DELTA_REFRESH: timedelta = timedelta(days=30)
    JWT_ALGORITHM: str = "RS256"
    JWT_PRIVATE_KEY: Path = BASE_DIR / "creds" / "jwt-private.pem"
    JWT_PUBLIC_KEY: Path = BASE_DIR / "creds" / "jwt-public.pem"


class GunicornConfig(BaseModel):
    port: int = 8888
    reload: bool = False
    host: str = "0.0.0.0"
    workers: int = 1
    timeout: int = 900
    workers_class: str = "uvicorn.workers.UvicornWorker"
    error_log: str | None = "-"
    access_log: str | None = "-"


class UvicornConfig(BaseModel):
    port: int = 8888
    host: str = "127.0.0.1"
    reload: bool = True


class GeneralAppConfig(BaseModel):
    title: str = "FastAPI JWT Authentication"
    mode: Literal["TEST", "DEV"]
    api_prefix: str = "/api"
    v1_prefix: str = "/v1"


class Settings(BaseSettings):
    db: DBConfig
    app: GeneralAppConfig
    auth: TokenConfig = TokenConfig()
    uvicorn: UvicornConfig = UvicornConfig()
    gunicorn: GunicornConfig = GunicornConfig()

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        extra="ignore",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="CFG_",
    )


settings = Settings()  # type: ignore
