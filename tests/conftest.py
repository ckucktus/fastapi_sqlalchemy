import asyncio
import pytest
from sqlalchemy.ext.asyncio.session import AsyncSession
from schemas.jobs import BaseJob
from sql_app.crud import Users_CRUD, Jobs_CRUD
from sql_app.models import Jobs, Users
from httpx import AsyncClient
from main import app
from sqlalchemy.exc import SQLAlchemyError
from sql_app.database import SessionLocal
from schemas.users import UserIn
from core.security import create_access_token
from sql_app.models import Users
from typing import Generator


@pytest.fixture(scope="session")
def event_loop(request) -> Generator:
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()



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








@pytest.fixture
async def create_user(db) -> Users:
    json = {
    "name": "test",
    "email": "test@mail.ru",
    "is_company": False,
    "password": "stringst",
    "password2": "stringst"
    }
    return  await create_user_or_company(json, db)

@pytest.fixture
async def create_company(db) -> Users:
    json = {
    "name": "test",
    "email": "jobs@mail.ru",
    "is_company": True,
    "password": "stringst",
    "password2": "stringst"
    }
    user = await create_user_or_company(json, db)
    
    return user

@pytest.fixture
async def create_job(create_company, db:AsyncSession) -> Jobs:
    json  = {
    "title": "Software Engineer",
    "description": "string",
    "salary_from": 1000,
    "salary_to": 5000,
    "is_active": True
    }
    user_id = create_company.id
    
    job =  await Jobs_CRUD.create(user_id, BaseJob.parse_obj(json),db)
    return job
    

@pytest.fixture
async def get_token(create_user, db) -> str:
    data = {"sub": str(create_user.id)}
    token = create_access_token(data)
    return token

def get_pydantic_obj_from_SA_obj(user:Users, pydantic_class):
    return pydantic_class.from_orm(user)

async def create_user_or_company(json, db):
    user = await Users_CRUD.get_by_email(json.get('email'), db)
    if not user:
        schema = UserIn.parse_obj(json)
        user = await Users_CRUD.create(schema, db)
    await db.commit()
    return user


   



#