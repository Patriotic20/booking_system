from fastapi import APIRouter , Depends , HTTPException , status
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.base import get_db
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from src.models import Booking , User 
from src.utils.auth import get_current_user


read_router = APIRouter()


@read_router.get("/get-all")
async def get_oprder(
    user_data: User = Depends(get_current_user),
    db : AsyncSession = Depends(get_db)):
    try:
        order = await db.execute(select(Booking).where(Booking.user_id == user_data.id))
        result = order.scalars().all()

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No orders found for this user"
            )
        return result
    
    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error. Please try again later."
        )

@read_router.get("/get/{order_id}")
async def get_by_id(
    order_id : int,
    user_data : User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
    ):
    try:
        order = await db.execute(
            select(Booking)
            .where(
            (Booking.user_id == user_data.id) & 
            (Booking.id == order_id)
            ))
        result = order.scalars().first()

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No orders found for this user"
            )
        
        return result
    
    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error. Please try again later."
        )