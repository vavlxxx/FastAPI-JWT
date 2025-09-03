from fastapi import APIRouter

from src.api.v1.dependencies.auth import LoginData, UserDataByAccess, UserDataByRefresh
from src.services.auth import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication and Authorization"],
)


@router.post("/login/")
async def login(login_data: LoginData):
    """
    Login user
    """

    access_token = AuthService().create_access_token(
        payload={"sub": login_data.username, "hello": "world"}
    )
    refresh_token = AuthService().create_refresh_token(
        payload={"sub": login_data.username}
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


@router.get("/profile/")
async def get_profile(userdata: UserDataByAccess):
    """
    User's profile
    """
    return userdata


@router.get("/refresh/")
async def refresh(userdata: UserDataByRefresh):
    """
    Refresh token
    """
    access_token = AuthService().create_access_token(
        payload={"sub": userdata, "hello": "world"}
    )
    refresh_token = AuthService().create_refresh_token(payload={"sub": userdata})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }
