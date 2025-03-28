from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.core.base import get_db
from src.models.store import Store

delete_router = APIRouter()

@delete_router.delete("/delete/{store_id}")
async def delete_store(
    store_id: int,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(select(Store).where(Store.id == store_id))
    store = result.scalars().first()
    

    if not store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Store not found"
        )
    
    try:
        await db.delete(store)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Delete error: {e}"
        )
    
    return {"message": "Store deleted successfully"}
