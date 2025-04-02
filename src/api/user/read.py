from fastapi import APIRouter, Depends, HTTPException, status
from src.core.base import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from src.utils.auth import check_user_role
from src.models import User 
from sqlalchemy.future import select
from src.schemas.user import UserResponse

read_router = APIRouter()

@read_router.get("/get-all", response_model=list[UserResponse])
async def read_users(
    user_role: User = Depends(check_user_role(["owner"])),
    db: AsyncSession = Depends(get_db)
):
    try:
        result = await db.execute(select(User))
        users = result.scalars().all()

        if not users:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Users not found"
            )

        return users

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error: {str(e)}"
        )

@read_router.get("/get/{user_id}", response_model=UserResponse)
async def get_by_id(
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
                detail="User not found"
            )

        return user

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error: {str(e)}"
        )
