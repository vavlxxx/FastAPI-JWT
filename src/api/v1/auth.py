import secrets

from fastapi import APIRouter, HTTPException

from src.api.v1.dependencies.auth import LoginData, UserData
from src.config import settings
from src.services.auth import AuthService
from src.utils.temp_users import users

router = APIRouter(
    prefix="/auth",
    tags=["Authentication and Authorization"],
)


@router.post("/login/")
async def login(login_data: LoginData):
    """
    Login user
    """
    user_password: str | None = users.get(login_data.username, None)
    if user_password is None:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    is_match = secrets.compare_digest(login_data.password, user_password)
    if not is_match:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    token = AuthService().generate_token(
        payload={"sub": login_data.username},
        expires_delta=settings.JWT_EXPIRE_DELTA_ACCESS,
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }


@router.get("/profile/")
async def get_profile(userdata: UserData):
    """
    User's profile
    """
    return userdata
