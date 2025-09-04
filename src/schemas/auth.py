from datetime import datetime
from enum import Enum
from typing import Annotated

from fastapi import Form
from pydantic import EmailStr

from src.schemas.base import BaseDTO


class UserLoginDTO(BaseDTO):
    username: str
    password: str


class UserDTO(UserLoginDTO):
    id: int
    first_name: str
    last_name: str
    birth_date: datetime
    email: EmailStr
    bio: str


class UserWithPasswordDTO(UserDTO):
    hashed_password: str


class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"


LoginData = Annotated[UserLoginDTO, Form()]
