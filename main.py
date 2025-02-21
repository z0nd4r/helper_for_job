from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import uvicorn

from contextlib import asynccontextmanager

import logging

from app.datadase.database import engine, Base
# from app.api.users.views import router as crud_users
from app.api.auth.views import router as auth
from app.api.channels.views import router as crud_channels


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
        logger.info("Database tables created (or already exist).")
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

# app.include_router(crud_users)
app.include_router(auth)
app.include_router(crud_channels)

# Домены, с которых разрешены запросы
origins = [
    # "http://localhost:3000",  # Для локальной разработки React
    "https://qsoops.github.io", # Домен фронтенда
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