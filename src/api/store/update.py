from fastapi import APIRouter , Depends , HTTPException , status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.core.base import get_db
from src.schemas.store import StoreUpdate
from src.models.store import Store




update_router = APIRouter()


@update_router.put("/update")
async def update_store(
    store_id: int,
    update_items: StoreUpdate,
    db: AsyncSession = Depends(get_db)
    ):
    result = await db.execute(select(Store).where(Store.id == store_id))
    store = result.scalars().first()

    if store is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Store not found"
        )
    
    update_data = update_items.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr( store , key , value)

    try:
        db.add(store)
        await db.commit()
        await db.refresh(store)
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail= f"Update error {e}"
        )
    return store
