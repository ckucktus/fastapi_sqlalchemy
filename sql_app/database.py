from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.sql.schema import MetaData

SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://test:Xbcnjlkz,l1@0.0.0.0/labor_exchange"

Base = declarative_base()

engine = create_async_engine(SQLALCHEMY_DATABASE_URL,future=True, echo=True)

SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

metadata = MetaData()
# a = SessionLocal()
# print(isinstance(a, AsyncSession))


async def startup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)



