from fastapi import APIRouter
from .delete import delete_router
from .read import read_router
from .update import update_router
from .create import create_router


user_router = APIRouter(
    tags=["User"],
    prefix="/user"
)

user_router.include_router(delete_router)
user_router.include_router(read_router)
user_router.include_router(update_router)
user_router.include_router(create_router)

