from fastapi import APIRouter , Depends , HTTPException , status
from src.core.base import get_db
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.booking import BookingUpdate
from src.models import Booking , User
from src.utils.auth import get_current_user
from sqlalchemy.exc import SQLAlchemyError


update_router = APIRouter()

@update_router.put("/update")
async def update(
    update_item: BookingUpdate,
    user_data: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
    ):
    try:
        result = await db.execute(select(Booking).where(
            (Booking.id == update_item.id)
            &
            (Booking.user_id == user_data.id)
        ))
        order = result.scalars().first()

        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Order with ID {update_item.id} not found."
            )



        update_data = update_item.model_dump(exclude_unset=True)
        for key , value in update_data.items():
            setattr(order , key , value)

        await db.commit()
        await db.refresh(order)

        return {"message": "Order updated successfully", "order": order}
    
    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail= "Database error. Please try again later."
        )

