import asyncio
from fastapi.exceptions import HTTPException
from fastapi import Depends, status, FastAPI
import pytest
from sqlalchemy.ext.asyncio.session import AsyncSession
from asgi_lifespan import LifespanManager
from dependency import get_db, decode_access_token
from sql_app.crud import Users_CRUD, Jobs_CRUD
from httpx import AsyncClient
from main import app
from sqlalchemy.exc import SQLAlchemyError
from sql_app.database import SessionLocal
from schemas.users import UserIn
from core.security import create_access_token, decode_access_token
from sql_app.models import Users
from typing import Generator

'''мне пригодится 
фикстура для получения юзера (передаю туда токен из которого вытаскивается id и делается запрос к бд)
1) генерация токена для гет каррент юзера(импорт уже готовой функции)
2)
'''
@pytest.fixture(scope="session")
def event_loop(request) -> Generator:
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

# @pytest.fixture
# async def get_current_user(token: str, db:AsyncSession = Depends(get_db)):
#     cred_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Credentials are not valid")
#     payload = decode_access_token(token)
#     if payload is None:
#         raise cred_exception
#     user_id: int = int(payload.get("sub"))
#     if user_id is None:
#         raise cred_exception
#     user = await Users_CRUD.get_by_id(user_id, db)
#     if user is None:
#         return cred_exception
#     return user

# @pytest.fixture
# async def client() -> AsyncClient:  #(app: FastAPI)
#     async with LifespanManager(app):
#         async with AsyncClient(
#             app=app, base_url="http://testserver", headers={"Content-Type": "application/json"}
#         ) as ac:
#             yield ac

@pytest.fixture
async def client() -> AsyncClient:  #(app: FastAPI)
    async with AsyncClient(
        app=app, base_url="http://testserver", headers={"Content-Type": "application/json"}
    ) as ac:
        yield ac

@pytest.fixture
async def db():
    session = SessionLocal()
    try:
        yield  session
        await session.commit()
    except SQLAlchemyError as ex:
        await session.rollback()
        raise ex
    finally:
        await session.close()

# @pytest.fixture
# async def userIN(db) -> users.UserIn:
#     json = {
#     "name": "test",
#     "email": "test@mail.ru",
#     "is_company": True,
#     "password": "stringst",
#     "password2": "stringst"
#     }

#     user = await Users_CRUD.get_by_email('test@mail.ru', db)############'''l'''
#     await db.delete(user)
#     if not user:
#         schema = users.UserIn.parse_obj(json)
#         user = await Users_CRUD.create(schema, db)
#         return user
#     return users.UserIn.from_orm(user)

def get_pydantic_obj_from_SA_obj(user:Users, pydantic_class):
    return pydantic_class.from_orm(user)


# @pytest.fixture
# async def create_user(db) -> UserIn:
#     json = {
#     "name": "test",
#     "email": "test@mail.ru",
#     "is_company": True,
#     "password": "stringst",
#     "password2": "stringst"
#     }
#     return await get_pydantic_obj_from_SA_obj(json, UserIn, db)

@pytest.fixture
async def create_user(db) -> Users:
    json = {
    "name": "test",
    "email": "test@mail.ru",
    "is_company": True,
    "password": "stringst",
    "password2": "stringst"
    }
    user = await Users_CRUD.get_by_email(json.get('email'), db)
    # await db.delete(user)
    if not user:
        schema = UserIn.parse_obj(json)
        user = await Users_CRUD.create(schema, db)
    await db.commit()
    return user


@pytest.fixture
async def get_token(create_user, db) -> str:
    data = {"sub": str(create_user.id)}
    token = create_access_token(data)
    return token





#