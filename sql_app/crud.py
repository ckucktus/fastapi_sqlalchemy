from sqlalchemy import update, select, delete, insert
from .models import Jobs, Users
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.jobs import Job, JobIn, BaseJob
from schemas.users import UserIn
from typing import List
from core.security import hash_password
import datetime

class Jobs_CRUD:

    @staticmethod
    async def get_list_of_jobs(offset:int , limit:int, db:AsyncSession):
        query = select(Jobs).offset(offset).limit(limit)
        return await db.execute(query)

    @staticmethod
    async def get_job_by_id(pk: int, db: AsyncSession):
        # query = db.query(Jobs).get(pk)
        # result = await db.execute(query)  # тут работает по айди
        # return result
        query = select(Jobs).where(Jobs.id == pk)
        result = await db.execute(query)
        if result:
            return result.first()[0]

    @staticmethod
    async def create(user_id: int, job:BaseJob, db:AsyncSession ) -> Jobs:
        new_job = job.dict()
        new_job['user_id'] = user_id
        query = insert(Jobs).values(new_job)
        result = await db.execute(query)
        new_job['id'] = result.inserted_primary_key[0]
        return new_job

        # new_job = Jobs(
        #     user_id = user_id,
        #     title = job.title,
        #     description = job.description,
        #     salary_from=job.salary_from,
        #     salary_to=job.salary_to,
        #     is_active=job.is_active
        # )
        # id = db.add(new_job)
        # print(id)
        #return new_job
        return None

    @staticmethod #редактировать может только создатель и суперюзер
    async def update_job(pk: int, job: BaseJob, db: AsyncSession) -> Jobs:
        updated_values = job.dict()
        updated_values['updated_at'] = datetime.datetime.now()
    
        query = update(Jobs).where(Jobs.id == pk).values(updated_values)
        result = await db.execute(query)
        return   {'id': pk, **result.last_updated_params()} #result.last_updated_params() # тут работает по айди
    
    @staticmethod
    async def delete_job(pk:int, db:AsyncSession): # тут работает по айди
        # query = delete(Jobs).where(Jobs.id == pk).returning(Jobs.id)
        job = await Jobs_CRUD.get_job_by_id(pk, db)
        await db.delete(job)
        return job

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
        result = result.first()
        if result:
            return result[0]

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
        updated_values['updated_at'] = datetime.datetime.now()
        query = update(Users).where(Users.id == pk).values(updated_values)
        result = await db.execute(query)
        return result.last_updated_params()

    @staticmethod
    async def get_by_email(email: str, db:AsyncSession) -> Users:
        query = select(Users).where(Users.email == email)
        result = await db.execute(query)
        result = result.first()
        if result:
            return result[0]
