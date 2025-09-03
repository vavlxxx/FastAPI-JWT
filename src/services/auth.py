from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException
from jwt.exceptions import ExpiredSignatureError

from src.config import settings


class AuthService:
    def generate_token(
        self,
        payload: dict,
        expires_delta: timedelta,
    ) -> str:
        token_data = payload.copy()
        now = datetime.now(timezone.utc)
        token_data["exp"] = datetime.timestamp(now + expires_delta)
        token_data["iat"] = datetime.timestamp(now)

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
