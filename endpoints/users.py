from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql.expression import true
from dependency import get_db, get_current_user
from schemas.users import BaseUser, UserIn
from sql_app.crud import Users_CRUD
from sql_app.models import Users

router = APIRouter()


@router.post('create', response_model=BaseUser)
async def create_user(user: UserIn, db:AsyncSession = Depends(get_db)):
    return await Users_CRUD.create(user, db)

@router.put('update', response_model=BaseUser)
async def update_user(user: UserIn, 
    current_user = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db)):
    print(current_user.id, '_'*100)
    updated_user = await Users_CRUD.update(current_user.id, user, db)
    print(type(update_user))
    print(update_user.__dict__)

    return updated_user

@router.get('/')
async def get_user_by_id():
    return None

@router.get('/list_users/', response_model=List[BaseUser])
async def show_users(offset:int, limit:int, db:AsyncSession = Depends(get_db)):
    result = await Users_CRUD.get_all(offset, limit, db) 
    return result.scalars().all()

