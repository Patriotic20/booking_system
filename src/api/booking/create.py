from fastapi import APIRouter , Depends  , HTTPException , status
from src.core.base import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.booking import BookingCreate
from src.models import Booking , User 
from src.utils.auth import get_current_user
from sqlalchemy.exc import SQLAlchemyError



create_router = APIRouter()

@create_router.post("/create")
async def booking_create(
    booking_item: BookingCreate,
    user_data: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        new_booking = Booking(
            user_id = user_data.id,
            store_id = booking_item.store_id,
            order_details = booking_item.order_details
        )

        db.add(new_booking)
        await db.commit()
        await db.refresh(new_booking)

        return new_booking
    
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Databse error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )
 