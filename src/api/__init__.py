from fastapi import APIRouter
from .store import store_router
from .booking import booking_router
from .auth import auth_router
from .user import user_router

main_router = APIRouter()


main_router.include_router(store_router)
main_router.include_router(booking_router)
main_router.include_router(auth_router)
main_router.include_router(user_router)