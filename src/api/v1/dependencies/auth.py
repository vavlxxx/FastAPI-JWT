from typing import Annotated

from fastapi import Depends, Form, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.schemas.auth import UserLoginDTO
from src.services.auth import AuthService
from src.utils.temp_users import users

_bearer = HTTPBearer()
BearerCredentials = Annotated[HTTPAuthorizationCredentials, Depends(_bearer)]

LoginData = Annotated[UserLoginDTO, Form()]


def get_payload_from_token(creds: BearerCredentials):
    token = creds.credentials
    token_payload = AuthService().decode_token(token)
    return token_payload


def get_userdata_from_payload(payload: dict = Depends(get_payload_from_token)):
    username = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    return users[username]


UserData = Annotated[str, Depends(get_userdata_from_payload)]
