from typing import Annotated

from fastapi import Depends, Form
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.schemas.auth import UserLoginDTO

_bearer = HTTPBearer()
BearerCredentials = Annotated[HTTPAuthorizationCredentials, Depends(_bearer)]

LoginData = Annotated[UserLoginDTO, Form()]
