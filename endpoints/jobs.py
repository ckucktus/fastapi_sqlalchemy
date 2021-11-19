from typing import List
from schemas.jobs import Job, JobIn, JobOut
from fastapi import APIRouter, Depends, HTTPException, status, Query
from schemas.jobs import BaseJob
from sqlalchemy.ext.asyncio import AsyncSession
from dependency import get_current_user, get_db
from sql_app.crud import Jobs_CRUD
from sql_app.models import Users


router = APIRouter()

@router.post('create', response_model=JobOut)
async def create_job(job:BaseJob, current_user:Users = Depends(get_current_user),
         db:AsyncSession = Depends(get_db)):
    if current_user.is_company:
        new_job = await Jobs_CRUD.create(current_user.id, job, db )
        return new_job
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Only companies can post vacancies')

@router.get('get_list', response_model=List[JobOut])
async def get_list_jobs(offset:int = Query(..., ge=0), limit:int = Query(..., ge=0), db: AsyncSession = Depends(get_db)):
    result = await Jobs_CRUD.get_list_of_jobs(offset, limit, db)
    result = result.scalars().all()
    if result:
        return result
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='Jobs not found')

@router.get('by_id', response_model=JobOut)
async def get_job_by_id(pk: int = Query(..., ge=0), db: AsyncSession = Depends(get_db)):
    result =  await Jobs_CRUD.get_job_by_id(pk, db)
    result = result.scalars().all()
    if result:
        return result
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='Jobs not found')

@router.put('update', response_model=JobOut)
async def update_job(id: int, input_job:BaseJob, current_user = Depends(get_current_user),
         db: AsyncSession = Depends(get_db)): 
    '''обновлять  вакансии могут владельцы или суперюзер'''

    job = await Jobs_CRUD.get_job_by_id(id, db)
    if job.user_id == current_user.id: # тут еще будет проверка на суперпользователя
        updated_job = await Jobs_CRUD.update_job(id, input_job, db)        
        return updated_job
    else:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail="User Without enough privileges" )

@router.delete('delete', response_model=JobOut)
async def delete_job(id: int, current_user = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    '''удалять  вакансии могут владельцы или суперюзер'''
    job = await Jobs_CRUD.get_job_by_id(id, db)
    if job:
        if job.user_id == current_user.id:
            result = await Jobs_CRUD.delete_job(id, db)
            return result
        else:
            raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail="User Without enough privileges" )
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This job does not exist")