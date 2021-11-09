from sqlalchemy import update, select
from sqlalchemy.sql.expression import Update
from .models import Jobs, Users
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.jobs import Job, JobIn
from schemas.users import UserIn
from typing import List
from core.security import hash_password

class Jobs_CRUD:

    @staticmethod
    async def get_data_by_id(db: AsyncSession, pk: int):
        query = db.query(Jobs).get(pk)
        result = await db.execute(query)
        return result

    @staticmethod
    async def create(db:AsyncSession, job:Job ):
        new_job = Jobs(
            user_id = job.user_id,
            title = job.title,
            description = job.description,
            salary_from=job.salary_from,
            salary_to=job.salary_to,
            is_active=job.is_active
        )
        db.add(new_job)
        return new_job

class Users_CRUD:

    @staticmethod
    async def get_all( offset:int , limit:int, db:AsyncSession) -> List[Users]:
        query = select(Users).offset(offset).limit(limit)
        # result = await db.execute(query)
        # print(result.scalars().all(), '-'*100)
        # result = result.scalars().all()
        return   await db.execute(query)

    @staticmethod
    async def get_by_id(pk:int, db:AsyncSession) -> Users:
        query = select(Users).where(Users.id == pk)
        result = await db.execute(query)
        return result.first()[0]

    @staticmethod
    async def create(user: UserIn, db:AsyncSession) -> Users:
        new_user = Users(
            email = user.email,
            name = user.name,
            hashed_password = hash_password(user.password2),
            is_company = user.is_company
        )
        db.add(new_user)
        return new_user

    @staticmethod
    async def update(pk:int, user: UserIn, db:AsyncSession) -> Users: #меня тут немного смущает что польователю придется вводить дважды пароль 
        updated_values = user.dict(exclude={'password2'})
        hashed_password = hash_password(updated_values.pop('password'))
        updated_values['hashed_password'] = hashed_password
        query = update(Users).where(Users.id == pk).values(updated_values).\
            returning(Users.name, Users.email, Users.is_company)
        result = await db.execute(query)
        return result.last_updated_params()

    @staticmethod
    async def get_by_email(email: str, db:AsyncSession) -> Users:
        query = select(Users).where(Users.email == email)
        result = await db.execute(query)
        return result.first()[0]