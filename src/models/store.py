from sqlalchemy import Column, String , Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from src.core.base import Base
from src.models.store_user import user_store_association


class Store(Base):
    __tablename__ = "stores"

    id = Column(Integer , primary_key=True , nullable=False)
    name = Column(String , nullable=False)
    description = Column(String , nullable=False)
    liter_price = Column(JSONB , nullable=False)
    
    users = relationship("User" , secondary=user_store_association , back_populates='stores')