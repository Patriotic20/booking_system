from fastapi import APIRouter , Depends , HTTPException , status
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.base import get_db
from src.schemas.store import StoreCreate , StoreResponse
from sqlalchemy.exc import SQLAlchemyError
from src.utils.store import get_existing_by_name
from src.models.store import Store


create_router = APIRouter()


@create_router.post("/create")
async def create_store(
    store_item: StoreCreate,
    db : AsyncSession = Depends(get_db)):


    if await get_existing_by_name( db , model_name=Store , name=store_item.name):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail="Store already have"
                )

        
    new_store = Store(**store_item.model_dump(exclude_unset=True))
    db.add(new_store)
    try:
        await db.commit()
        await db.refresh(new_store)
    except SQLAlchemyError as e:
         await db.rollback()
         raise HTTPException(
              status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
              detail=f"Database error: {str(e)}"
         )
    return StoreResponse.model_validate(new_store)