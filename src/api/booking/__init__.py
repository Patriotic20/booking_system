from fastapi import APIRouter
from .create import create_router
from .update import update_router
from .read import read_router
from .delete import delete_router


booking_router = APIRouter(
    tags=["Booking"],
    prefix="/booking"
)


booking_router.include_router(create_router)
booking_router.include_router(update_router)
booking_router.include_router(read_router)
booking_router.include_router(delete_router)

