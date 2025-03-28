from fastapi import APIRouter , Depends 
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.base import get_db
from sqlalchemy.future import select
from src.models.store import Store
from src.schemas.store import StoreResponse
from typing import List




read_router = APIRouter()


@read_router.get("/get" , response_model=List[StoreResponse])
async def get_store(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Store).limit(100))
    stores = result.scalars().all()
    return stores


@read_router.get("/get/{store_id}")
async def get_all(
    store_id: int,
    db : AsyncSession = Depends(get_db)):

    result = await db.execute(select(Store).where(Store.id == store_id))
    store  = result.scalars().first()
    return store


