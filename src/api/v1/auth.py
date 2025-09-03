from fastapi import APIRouter

router = APIRouter(
    prefix="/auth",
    tags=["Authentication and Authorization"],
)


@router.post("/login/")
async def login():
    """
    Login user
    """
    return


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
