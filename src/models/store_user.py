from sqlalchemy import Table , Column , Integer , ForeignKey
from src.core.base import Base

user_store_association = Table(
    'user_store_association', Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("store_id", Integer, ForeignKey("stores.id"), primary_key=True)    
)