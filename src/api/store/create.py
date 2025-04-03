from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import insert
from sqlalchemy.future import select
from src.core.base import get_db
from src.schemas.store import StoreCreate, StoreResponse
from src.utils.store import get_existing_by_name
from src.utils.auth import get_current_user, check_user_role
from src.models import Store, User, user_store_association

create_router = APIRouter()

@create_router.post("/create", response_model=StoreResponse)
async def create_store(
    store_item: StoreCreate,
    user_data: User = Depends(get_current_user),
    user_role: User = Depends(check_user_role(["owner"])),
    db: AsyncSession = Depends(get_db)
):
    try:
        result = await db.execute(select(Store).where(Store.name == store_item.name))
        store = result.scalars().first()

        if store:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail="Store already exists"
            )

        
        new_store = Store(**store_item.model_dump(exclude_unset=True))
        db.add(new_store)
        await db.flush()  

        
        stmt = insert(user_store_association).values(user_id=user_data.id, store_id=new_store.id)
        await db.execute(stmt)

        
        await db.commit()


        return StoreResponse(**new_store.__dict__)

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )