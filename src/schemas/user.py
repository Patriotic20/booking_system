from pydantic import BaseModel , Field
from datetime import datetime
from src.models.user import UserRole

class UserBase(BaseModel):
    phone_number : str 
    city : str
    street: str | None = Field(None , min_length=3)
    flat : str | None = Field(None , min_length=1)
    home_number : str |None = Field(None)



class UserOwner(UserBase):
    password: str
    role: UserRole

class UserCrate(UserBase):
    password: str



class UserUpdate(BaseModel):
    id: int
    phone_number : str | None = None
    city : str | None = None
    street: str | None = None
    flat : str | None = None
    home_number : str | None = None

class UserResponse(UserBase):
    id: int
    create_at: datetime


    class Config:
        from_attributes = True 