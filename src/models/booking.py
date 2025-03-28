from sqlalchemy import Column , String , Integer , ForeignKey , DateTime
from sqlalchemy.dialects.postgresql import JSONB
from src.core.base import Base
from datetime import datetime

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer , primary_key=True , nullable=False)
    user_id = Column(Integer , ForeignKey("users.id") , nullable=False)
    store_id = Column(Integer, ForeignKey("stores.id") , nullable=False)
    order_details = Column(JSONB , nullable=False)
    create_at = Column(DateTime , default=datetime.now)
    