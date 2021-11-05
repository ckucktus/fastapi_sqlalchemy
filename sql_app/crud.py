from .models import Jobs, Users
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class Jobs_CRUD():
    async def get_data(db:AsyncSession, pk:int):
        #query = select(Jobs).all()
        query = db.query(Jobs).get(pk)
        result = await db.execute(query)
        return result
