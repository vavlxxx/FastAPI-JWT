from enum import Enum

from src.schemas.base import BaseDTO


class UserLoginDTO(BaseDTO):
    username: str
    password: str


class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"
