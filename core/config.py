from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL:str = 'postgresql+asyncpg://test:Xbcnjlkz,l1@ckucktus/fastapi'
    