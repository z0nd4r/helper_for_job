import os

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv

load_dotenv()

DATABASE_USER = os.getenv("POSTGRES_USER")
DATABASE_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DATABASE_HOST = os.getenv("POSTGRES_HOST")
DATABASE_PORT = os.getenv("POSTGRES_PORT")
DATABASE_NAME = os.getenv("POSTGRES_NAME")

SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

engine = create_async_engine(
    url=SQLALCHEMY_DATABASE_URL,
    echo=False,
    echo_pool=False,
    max_overflow=10, # сколько дополнительных соединений может быть создано, когда пул соединений исчерпан
    pool_size=10, # размер пула соединений
)
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)





