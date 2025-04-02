from fastapi import APIRouter , Depends , HTTPException , status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from src.core.base import get_db
from src.utils.auth import authenticate_user , create_access_token , create_refresh_token
from datetime import timedelta
from src.core.config import settings

login_router = APIRouter()


@login_router.post("/login")
async def login(
    from_data : OAuth2PasswordRequestForm = Depends(),
    db : AsyncSession = Depends(get_db)):

    user = await authenticate_user(
        db=db , 
        username=from_data.username , 
        password=from_data.password
        )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not unauthorized"
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)




    access_token = await create_access_token(
        {
            "sub": user.phone_number,
            "role": user.role.value
        },
        access_token_expires
        
    )

    refresh_token = await create_refresh_token(
        {
            "sub" : user.phone_number,
            "role" : user.role.value
        },
        refresh_token_expires
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }  
    