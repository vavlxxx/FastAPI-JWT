import secrets

from fastapi import APIRouter, HTTPException

from src.api.v1.dependencies.auth import LoginData
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
        raise HTTPException(status_code=401, detail="Incorrect username or password")  # noqa: F821

    is_match = secrets.compare_digest(login_data.password, user_password)
    if not is_match:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    return login_data


@router.get("/profile/")
async def get_profile():
    """
    User's profile
    """
    return


@router.post("/logout/")
async def logout():
    """
    Logout user
    """
    return
