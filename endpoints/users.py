from os import stat
from typing import List
from fastapi import APIRouter, Depends, status
from fastapi.param_functions import Query
from sqlalchemy.ext.asyncio.session import AsyncSession
from dependency import get_db, get_current_user
from schemas.users import BaseUser, UserIn
from sql_app.crud import Users_CRUD
from fastapi.exceptions import HTTPException

router = APIRouter()


@router.post('create', response_model=BaseUser)
async def create_user(user: UserIn, db:AsyncSession = Depends(get_db)):
    return await Users_CRUD.create(user, db)

@router.put('update', response_model=BaseUser)
async def update_user(user: UserIn, 
    current_user = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db)):
    updated_user = await Users_CRUD.update(current_user.id, user, db)

    return updated_user

@router.get('/', response_model=BaseUser)
async def get_user_by_id(pk:int, db: AsyncSession = Depends(get_db)):
    result = await Users_CRUD.get_by_id(pk, db)
    if result:
        result
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

@router.get('/list_users/', response_model=List[BaseUser])
async def show_users(offset:int = Query(..., ge=0), limit:int = Query(..., ge=0), db:AsyncSession = Depends(get_db)):
    result = await Users_CRUD.get_all(offset, limit, db) 
    result = result.scalars().all()
    if result:
        return result
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='Users not found')

