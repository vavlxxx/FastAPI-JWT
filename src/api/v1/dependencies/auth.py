from typing import Annotated

from fastapi import Depends, Form, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.schemas.auth import TokenType, UserLoginDTO
from src.services.auth import AuthService

_bearer = HTTPBearer()

BearerCredentials = Annotated[HTTPAuthorizationCredentials, Depends(_bearer)]
LoginData = Annotated[UserLoginDTO, Form()]


class TypedTokenParser:
    def __init__(self, token_type: TokenType):
        self.expected_type = token_type

    def get_payload_from_token(self, creds: BearerCredentials):
        token = creds.credentials
        token_payload = AuthService().decode_token(token)
        return token_payload

    def get_user_data_from_payload(self, payload: dict):
        user_data = payload.get("sub")
        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token without sub field",
            )
        return user_data

    def compare_token_type_with_payload(
        self,
        payload: dict,
    ) -> bool:
        token_type = payload.get("type")
        if not token_type:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token without type",
            )
        if token_type != self.expected_type:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type, got: {}, expected: {}".format(
                    token_type,
                    self.expected_type,
                ),
            )
        return True

    def __call__(
        self,
        payload: dict = Depends(get_payload_from_token),
    ) -> str:
        self.compare_token_type_with_payload(payload)
        return self.get_user_data_from_payload(payload)


UserDataByAccess = Annotated[str, Depends(TypedTokenParser(TokenType.ACCESS))]
UserDataByRefresh = Annotated[str, Depends(TypedTokenParser(TokenType.REFRESH))]
