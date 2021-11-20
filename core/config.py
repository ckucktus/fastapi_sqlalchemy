from pydantic import BaseSettings

class Settings(BaseSettings):
    #DATABASE_URL: str = 'postgresql+asyncpg://test:Xbcnjlkz,l1@ckucktus/fastapi'
    #ACCESS_TOKEN_EXPIRE_MINUTES: int = 120
    #SECRET_KEY: str = 'sugar'
    ALGORITHM: str = 'HS256'

settings = Settings()