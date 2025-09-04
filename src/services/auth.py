import secrets
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException
from jwt.exceptions import ExpiredSignatureError

from src.config import settings
from src.schemas.auth import LoginData, TokenType
from src.utils.temp_users import users


class AuthService:
    def create_access_token(self, payload: dict) -> str:
        return self._generate_token(
            payload=payload,
            expires_delta=settings.JWT_EXPIRE_DELTA_ACCESS,
            type=TokenType.ACCESS,
        )

    def create_refresh_token(self, payload: dict) -> str:
        return self._generate_token(
            payload=payload,
            expires_delta=settings.JWT_EXPIRE_DELTA_REFRESH,
            type=TokenType.REFRESH,
        )

    def _generate_token(
        self,
        payload: dict,
        expires_delta: timedelta,
        type: TokenType,
    ) -> str:
        token_data = payload.copy()
        now = datetime.now(timezone.utc)
        token_data["exp"] = datetime.timestamp(now + expires_delta)
        token_data["iat"] = datetime.timestamp(now)
        token_data["type"] = type

        return jwt.encode(
            payload=token_data,
            key=settings.JWT_PRIVATE_KEY.read_text(),
            algorithm=settings.JWT_ALGORITHM,
        )

    def decode_token(self, token: str) -> dict:
        try:
            decoded_token = jwt.decode(
                jwt=token,
                key=settings.JWT_PUBLIC_KEY.read_text(),
                algorithms=(settings.JWT_ALGORITHM),
            )
        except ExpiredSignatureError as exc:
            raise HTTPException(status_code=401, detail=str(exc))
        return decoded_token

    async def login_user(self, login_data: LoginData):
        user_password: str | None = users.get(login_data.username, None)
        if user_password is None:
            raise HTTPException(
                status_code=401, detail="Incorrect username or password"
            )

        is_match = secrets.compare_digest(login_data.password, user_password)
        if not is_match:
            raise HTTPException(
                status_code=401, detail="Incorrect username or password"
            )

        access_token = AuthService().create_access_token(
            payload={"sub": login_data.username}
        )
        refresh_token = AuthService().create_refresh_token(
            payload={"sub": login_data.username}
        )

        return (access_token, refresh_token)
