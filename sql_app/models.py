import sqlalchemy
from sqlalchemy import DateTime
#from sql_app.class_base import Base
from .database import metadata, Base
from sqlalchemy import func




class Jobs(Base):
    __tablename__ = 'jobs'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=False)
    title = sqlalchemy.Column(sqlalchemy.String)
    description = sqlalchemy.Column(sqlalchemy.String)
    salary_from = sqlalchemy.Column(sqlalchemy.Integer)
    salary_to = sqlalchemy.Column(sqlalchemy.Integer)
    is_active = sqlalchemy.Column(sqlalchemy.Boolean)
    created_at = sqlalchemy.Column(DateTime, server_default=func.now())
    updated_at = sqlalchemy.Column(DateTime, server_default=func.now())

class Users(Base):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True)
    email = sqlalchemy.Column(sqlalchemy.String, primary_key=True, unique=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    hashed_password = sqlalchemy.Column(sqlalchemy.String)
    is_company = sqlalchemy.Column(sqlalchemy.Boolean)
    created_at = sqlalchemy.Column(DateTime, server_default=func.now())
    updated_at = sqlalchemy.Column(DateTime, server_default=func.now())
