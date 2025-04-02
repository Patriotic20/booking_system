from fastapi import APIRouter, Depends, HTTPException, status
from src.core.base import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from src.utils.auth import check_user_role
from src.models import User
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError

delete_router = APIRouter()

@delete_router.delete("/delete/{user_id}")
async def delete_user(
    user_id: int,
    user_role: User = Depends(check_user_role(["owner"])),
    db: AsyncSession = Depends(get_db)
):
    try:
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalars().first()

        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found."
            )

        
        await db.delete(user)
        await db.commit()

        return {"message": "User successfully deleted"}

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )



