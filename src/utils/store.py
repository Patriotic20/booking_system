from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


async def get_existing_by_name(db :AsyncSession , name: str , model_name: str):
    existing_store = await db.execute(select(model_name).where(model_name.phone_number == name))
    return existing_store.scalar_one_or_none()
