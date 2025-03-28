from fastapi import APIRouter
from .create import create_router 
from .read import read_router
from .update import update_router
from .delete import delete_router

store_router = APIRouter(
    prefix='/store',
    tags=["Store"]
)


store_router.include_router(create_router)
store_router.include_router(read_router)
store_router.include_router(update_router)
store_router.include_router(delete_router)