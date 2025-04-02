from fastapi import APIRouter , Depends , HTTPException , status
from src.core.base import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models import User 
from src.utils.auth import check_user_role
from src.schemas.user import UserUpdate , UserResponse
from sqlalchemy.exc import SQLAlchemyError


update_router = APIRouter()


@update_router.put("/update/{user_id}" , response_model=UserResponse)
async def update_user(
    user_items: UserUpdate,
    user_role: User = Depends(check_user_role([""])),
    db: AsyncSession = Depends(get_db)):

    try:

        result = await db.execute(select(User).where(User.id == user_items.id))
        user = result.scalars().first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user.id} not found."
            )
        update_data = user_items.model_dump(exclude_unset=True)
        for field , value in update_data.items():
            setattr(user , field , value)

        await db.commit()
        await db.refresh(user)

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

