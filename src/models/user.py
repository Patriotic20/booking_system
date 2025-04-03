from sqlalchemy import Column , String , Integer , Enum , DateTime 
from sqlalchemy.orm import relationship
from src.core.base import Base
from datetime import datetime
from src.models.store_user import user_store_association
import enum

class UserRole(enum.Enum):
    admin = "admin"
    user = "user"
    owner = "owner"
    courier = "courier"

    

class User(Base):
    __tablename__ = "users"

    id = Column(Integer , primary_key=True , nullable=False)
    phone_number = Column(String , nullable=False)
    password = Column(String , nullable=False)
    role = Column(Enum(UserRole) , default=UserRole.user , nullable=False)
    city = Column(String , nullable=False)
    street = Column(String , nullable=True)
    flat = Column(String , nullable=True)
    home_number = Column(String , nullable=True)
    create_at = Column(DateTime , default=datetime.now)

    stores = relationship("Store" , secondary=user_store_association , back_populates="users")

