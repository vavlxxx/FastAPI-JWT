from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import ExpiredSignatureError

from src.api.v1.dependencies.db import DBDep
from src.schemas.auth import TokenType
from src.services.auth import AuthService
from src.utils.exceptions import ObjectNotFoundError

_bearer = HTTPBearer()
BearerCredentials = Annotated[HTTPAuthorizationCredentials, Depends(_bearer)]


def _get_access_token(creds: BearerCredentials):
    token = creds.credentials
    try:
        return AuthService().decode_token(token)
    except ExpiredSignatureError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc),
        ) from exc


def _get_refresh_token(request: Request):
    token = request.cookies.get("refresh_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Missing refresh token",
        )

    try:
        return AuthService().decode_token(token)
    except ExpiredSignatureError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc),
        ) from exc


def _validate_token_type(payload: dict, expected_type: TokenType):
    token_type = payload.get("type")
    if not token_type or token_type != expected_type.value:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token type, expected: {expected_type.value}, got: {token_type}",
        )


def _extract_token_subject(payload: dict) -> str:
    username = payload.get("sub")
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing token subject field",
        )
    return username


def resolve_token_by_type(token_type: TokenType):
    if token_type == TokenType.ACCESS:

        def get_sub_from_access(creds: BearerCredentials):
            payload = _get_access_token(creds)
            _validate_token_type(payload, token_type)
            return _extract_token_subject(payload)

        return get_sub_from_access

    elif token_type == TokenType.REFRESH:

        async def get_sub_from_refresh(request: Request, db: DBDep):
            payload = _get_refresh_token(request)
            _validate_token_type(payload, token_type)
            uid = int(_extract_token_subject(payload))
            try:
                await db.tokens.get_one(owner_id=uid)
            except ObjectNotFoundError as exc:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Rejected refresh token, try to login again",
                ) from exc
            return uid

        return get_sub_from_refresh


UsernameByAccess = Annotated[str, Depends(resolve_token_by_type(TokenType.ACCESS))]
UidByRefresh = Annotated[int, Depends(resolve_token_by_type(TokenType.REFRESH))]
