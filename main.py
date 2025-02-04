from fastapi import FastAPI, Depends
import uvicorn
from app.Backend.api.database import engine, Base
from app.Backend.api.router import router

app = FastAPI()

app.include_router(router)

Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)