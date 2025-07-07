from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import uvicorn

from contextlib import asynccontextmanager

import logging

from starlette.staticfiles import StaticFiles

from app.datadase.database import engine
from app.datadase.models import Base
from app.api.auth.routers import router as auth
from app.api.channels.routers import router as crud_channels
from app.api.friends.routers import router as crud_friends


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def create_tables():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Tables created successfully!")
    except Exception as e:
        logger.error(f"Error creating tables: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Код, выполняемый при запуске приложения
    logger.info("Starting up...")
    try:
        await create_tables()
        logger.info("Database tables created")
        yield  # Приложение запущено и готово принимать запросы
    except Exception as e:
        logger.error(f"Startup failed: {e}")
        # В реальном приложении, возможно, следует выйти с ошибкой
        # чтобы предотвратить запуск неисправного приложения

    # Код, выполняемый при завершении приложения
    finally:
        logger.info("Shutting down...")
        await engine.dispose() # Закрытие соединения с базой данных
        logger.info("Database connection closed.")

app = FastAPI(lifespan=lifespan)

app.mount('/static', StaticFiles(directory='app/static'), name='static')

# app.include_router(crud_users)
app.include_router(auth)
app.include_router(crud_channels)
app.include_router(crud_friends)

# Домены, с которых разрешены запросы
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8080",  # Для локальной разработки React
    "http://127.0.0.1:8080", # Домен фронтенда
    # "https://your-frontend-domain.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # Разрешить передачу куки
    allow_methods=["*"],      # Разрешить все HTTP методы (GET, POST, PUT, DELETE, ...)
    allow_headers=["*"],      # Разрешить все заголовки
)


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)