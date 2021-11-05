from fastapi import FastAPI, Depends
import uvicorn
from sql_app import engine, Base, get_db, startup_db
from sqlalchemy.ext.asyncio import AsyncSession
from sql_app.crud import Jobs_CRUD

app = FastAPI()


@app.on_event("startup")
async def start_db():
    await startup_db()


@app.get('/checkdb')
async def check_db(db: AsyncSession = Depends(get_db)):
    return await Jobs_CRUD.get_data(db)



if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host = '0.0.0.0', reload = True)