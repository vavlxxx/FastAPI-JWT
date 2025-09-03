from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    UVICORN_PORT: int = 8000
    UVICORN_HOST: str = "127.0.0.1"
    UVICORN_RELOAD: bool = True


settings = Settings()
