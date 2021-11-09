from fastapi import APIRouter, HTTPException, status, Depends
from schemas.token import Token, Login
from sql_app.crud import Users_CRUD
from core.security import verify_password, create_access_token
from sqlalchemy.ext.asyncio import AsyncSession
from dependency import get_db

router = APIRouter()

@router.post("/", response_model=Token)
async def login(login: Login, db: AsyncSession = Depends(get_db)): 
    user = await Users_CRUD.get_by_email(login.email, db)
    if user is None or not verify_password(login.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

    return Token(
        access_token=create_access_token({"sub": str(user.id)}),
        token_type="Bearer"
    )