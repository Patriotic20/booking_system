from fastapi import APIRouter , Depends , HTTPException , status 
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.base import get_db
from src.schemas.user import UserCrate
from sqlalchemy.exc import SQLAlchemyError
from src.models.user import User
from src.utils.auth import get_user 


signup_router = APIRouter()


@signup_router.post("/signup")
async def signup(
    user_item : UserCrate,
    db: AsyncSession = Depends(get_db)):

    existing_user = await get_user(db , username = user_item.phone_number)

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already have in base"
        )

    new_user = User(**user_item.model_dump(exclude_unset=True))
    try:
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

    except SQLAlchemyError as e :
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error {e}"

        )
    return new_user
