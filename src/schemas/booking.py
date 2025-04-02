from pydantic import BaseModel
from typing import Dict
from datetime import datetime



class BookingBase(BaseModel):
    store_id: int
    order_details: Dict

class BookingCreate(BookingBase):
    pass

class BookingUpdate(BaseModel):
    id: int
    store_id: int | None = None
    order_details: Dict | None = None

class BookingResponse(BookingBase):
    id : int
    user_id : int
    create_at: datetime