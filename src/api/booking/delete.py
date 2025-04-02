from fastapi import APIRouter, Depends, HTTPException , status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from src.core.base import get_db
from src.models import User, Booking
from src.utils.auth import get_current_user

delete_router = APIRouter()

@delete_router.delete("/delete/{order_id}")
async def delete_order(
    order_id: int,
    user_data: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        
        result = await db.execute(
            select(Booking).where(
                (Booking.user_id == user_data.id) & (Booking.id == order_id)
            )
        )
        order = result.scalars().first()

        
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Order with ID {order_id} not found.")

        
        await db.delete(order)
        await db.commit()

        return {"message": "Order deleted successfully"}

    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Database error. Please try again later."
            )
