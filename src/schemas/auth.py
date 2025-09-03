from src.schemas.base import BaseDTO


class UserLoginDTO(BaseDTO):
    username: str
    password: str
