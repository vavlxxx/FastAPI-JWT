from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.schemas.auth import TokenType
from src.services.auth import AuthService

_bearer = HTTPBearer()
BearerCredentials = Annotated[HTTPAuthorizationCredentials, Depends(_bearer)]


def get_payload_from_token(creds: BearerCredentials):
    token = creds.credentials
    token_payload = AuthService().decode_token(token)
    return token_payload


def _get_user_data_from_payload(payload: dict):
    user_data = payload.get("sub")
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token without 'sub' field",
        )
    return user_data


class TypedTokenParser:
    def __init__(self, token_type: TokenType):
        self.expected_type = token_type

    def _compare_token_type_with_payload(
        self,
        payload: dict,
    ) -> bool:
        token_type = payload.get("type")
        if not token_type:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token without type",
            )
        if token_type != self.expected_type.value:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type, got: {}, expected: {}".format(
                    token_type,
                    self.expected_type.value,
                ),
            )
        return True

    def __call__(
        self,
        payload: dict = Depends(get_payload_from_token),
    ) -> str:
        self._compare_token_type_with_payload(payload)
        return _get_user_data_from_payload(payload)


UserDataByAccess = Annotated[str, Depends(TypedTokenParser(TokenType.ACCESS))]
UserDataByRefresh = Annotated[str, Depends(TypedTokenParser(TokenType.REFRESH))]
