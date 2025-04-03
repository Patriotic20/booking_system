from fastapi import APIRouter, Depends, HTTPException, status 
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from src.core.base import get_db
from src.schemas.user import UserOwner
from src.models import User 
from src.utils.auth import check_user_role


create_router = APIRouter()

@create_router.post("/create", response_model=UserOwner)
async def create_user(
    user_item: UserOwner,
    user_role: User = Depends(check_user_role(['owner'])),
    db: AsyncSession = Depends(get_db)
):
    try:
        result = await db.execute(select(User).where(User.phone_number == user_item.phone_number))
        existing_user = result.scalars().first()


        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User with phone number {user_item.phone_number} already exists."
            )
                
        new_user = User(**user_item.model_dump(exclude_unset=True))
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)  

        return new_user

    except SQLAlchemyError as e:
        await db.rollback()  
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )
