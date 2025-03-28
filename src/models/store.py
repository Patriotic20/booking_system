from sqlalchemy import Column, String , Integer
from sqlalchemy.dialects.postgresql import JSONB
from src.core.base import Base


class Store(Base):
    __tablename__ = "stores"

    id = Column(Integer , primary_key=True , nullable=False)
    name = Column(String , nullable=False)
    description = Column(String , nullable=False)
    liter_price = Column(JSONB , nullable=False)
    