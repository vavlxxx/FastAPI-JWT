from enum import Enum
from typing import Annotated

from fastapi import Form

from src.schemas.base import BaseDTO


class UserLoginDTO(BaseDTO):
    username: str
    password: str


class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"


LoginData = Annotated[UserLoginDTO, Form()]
