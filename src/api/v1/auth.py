from fastapi import APIRouter, Response

from schemas.auth import UserDTO
from src.api.v1.dependencies.auth import UidByRefresh, UsernameByAccess
from src.api.v1.dependencies.db import DBDep
from src.schemas.auth import LoginData, RegisterData, TokenResponseDTO
from src.services.auth import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication and Authorization"],
)


@router.post("/login/")
async def login(
    db: DBDep,
    login_data: LoginData,
    response: Response,
):
    """
    Login user
    """
    token_response: TokenResponseDTO = await AuthService(db).login_user(
        login_data=login_data,
        response=response,
    )

    return {
        "status": "ok",
        "data": {
            "access_token": token_response.access_token,
            "refresh_token": token_response.refresh_token,
            "token_type": "Bearer",
        },
    }


@router.post("/register/")
async def register(
    db: DBDep,
    register_data: RegisterData,
):
    """
    Register user
    """
    return await AuthService(db).register_user(register_data=register_data)


@router.get("/profile/")
async def get_profile(
    db: DBDep,
    username: UsernameByAccess,
) -> UserDTO:
    """
    User's profile
    """
    user = await AuthService(db).get_profile(username=username)
    return user


@router.get("/refresh/")
async def refresh(
    db: DBDep,
    uid: UidByRefresh,
    response: Response,
):
    """
    Refresh token
    """
    token_response: TokenResponseDTO = await AuthService(db).update_tokens(
        uid=uid,
        response=response,
    )

    return {
        "status": "ok",
        "data": {
            "access_token": token_response.access_token,
            "refresh_token": token_response.refresh_token,
            "token_type": "Bearer",
        },
    }
