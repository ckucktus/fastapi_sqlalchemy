import datetime
from pydantic import BaseModel
from typing import Optional

class BaseJob(BaseModel):
    title: str
    description: str
    salary_from: int
    salary_to: int
    is_active: bool = True

    class Config:
        orm_mode = True

class Job(BaseJob):
    id: int = None #id вакансии
    user_id: int #id создателя
    created_at: datetime.datetime = None
    updated_at: datetime.datetime = None

class JobOut(BaseJob):
    id: Optional[int]
    class Config:
        orm_mode = True


class JobIn(BaseJob):
    pass
    