from fastapi import APIRouter
from .login import login_router
from .singup import signup_router


auth_router = APIRouter(
    tags=["Auth"],
    prefix="/auth"
)

auth_router.include_router(login_router)
auth_router.include_router(signup_router)


