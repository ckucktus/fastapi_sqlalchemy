from typing import List
from schemas.jobs import Job, JobIn
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.jobs import BaseJob
from sqlalchemy.ext.asyncio import AsyncSession
from dependency import get_db
from sql_app.crud import Jobs_CRUD


router = APIRouter()

@router.post('/job/create', response_model=BaseJob)
async def create_job(job:Job, db:AsyncSession = Depends(get_db)):
    new_job = await Jobs_CRUD.create(db, job)
    # print(new_job)
    # print(new_job.__dict__)

    return new_job