from typing import AsyncGenerator

from sqlalchemy.ext.asyncio.session import AsyncSession
from sql_app.database import SessionLocal
from sqlalchemy.exc import SQLAlchemyError
from core.security import JWTBearer, decode_access_token
from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from sql_app.crud import Users_CRUD



async def get_db() -> AsyncGenerator:
    session = SessionLocal()
    try:
        yield  session
        await session.commit()
    except SQLAlchemyError as ex:
        await session.rollback()
        raise ex
    finally:
        await session.close()

async def get_current_user( # возвращает текущего пользователя расшифровывая его токен и вытаскивая из него id 
    token: str = Depends(JWTBearer()),
    db: AsyncSession = Depends(get_db)
    ):
    cred_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Credentials are not valid")
    payload = decode_access_token(token)
    if payload is None:
        raise cred_exception
    user_id: int = int(payload.get("sub"))
    if user_id is None:
        raise cred_exception
    user = await Users_CRUD.get_by_id(user_id, db)
    if user is None:
        return cred_exception
    return user