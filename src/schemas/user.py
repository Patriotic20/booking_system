from pydantic import BaseModel , field_validator
from datetime import datetime
import asyncio
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

class UserBase(BaseModel):
    phone_number : str
    city : str
    street: str
    flat : str
    home_number : str


class UserCrate(UserBase):
    password: str



class UserUpdate(BaseModel):
    phone_number : str | None = None 
    city : str | None = None
    street: str | None = None
    flat : str | None = None
    home_number : str | None = None

class UserResponse(UserBase):
    id: int
    create_at: datetime