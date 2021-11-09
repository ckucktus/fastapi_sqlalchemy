import datetime
from pydantic import BaseModel


class BaseJob(BaseModel):
    title: str
    description: str
    salary_from: int
    salary_to: int
    is_active: bool = True

    class Config:
        orm_mode = True

class Job(BaseJob):
    id: int = None
    user_id: int
    created_at: datetime.datetime = None
    updated_at: datetime.datetime = None


class JobIn(BaseJob):
    pass
    