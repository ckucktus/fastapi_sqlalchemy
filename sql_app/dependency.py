from typing import AsyncGenerator
from .database import SessionLocal
from sqlalchemy.exc import SQLAlchemyError


async def get_db() -> AsyncGenerator:
    session = SessionLocal()
    try:
        yield session
        await session.commit()
    except SQLAlchemyError as ex:
        await session.rollback()
        raise ex
    finally:
        await session.close()