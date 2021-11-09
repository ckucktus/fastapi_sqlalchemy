import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, validator, Field

# class User(BaseModel):
#     id: Optional[int] = None
#     name: str
#     email: EmailStr
#     hashed_password: str
#     is_company: bool
#     created_at: datetime.datetime = None
#     updated_at: datetime.datetime = None

class BaseUser(BaseModel):
    name: str
    email: EmailStr
    is_company: bool = False

    class Config:
        orm_mode = True


class UserIn(BaseUser):
    #name: str
    #email: EmailStr
    password: str = Field(..., min_length=8)   #constr(min_length=8)
    password2: str = Field(..., min_length=8)
    #is_company: bool = False

    @validator("password2")
    def password_match(cls, v, values, **kwargs):
        if 'password' in values and v != values["password"]:
            raise ValueError("passwords don't match")
        return v




    