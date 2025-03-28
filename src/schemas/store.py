from pydantic import BaseModel , Extra , Field
from typing import Dict

class StoreBase(BaseModel):
    name: str
    description: str
    liter_price : Dict[str , float] = Field(... , example={"10l" : 10})



class StoreCreate(StoreBase):
    pass

class StoreUpdate(BaseModel):
    name : str | None = None
    description : str | None = None
    liter_price: Dict[str , float] | None = Field(... , example = {"10l": 10})


class StoreResponse(StoreBase):
    id : int

    class Config:
        from_attributes = True