from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.exc import SQLAlchemyError

import asyncio

from .database import SQLALCHEMY_DATABASE_URL

class Database_Helper():
    def __init__(self, url: str):
        self.engine = create_async_engine(
            url=url,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def get_session(self) -> AsyncSession: # type: ignore
        async with self.session_factory() as session:
            try:
                yield session
            except SQLAlchemyError as e:
                # Обработка ошибок, печать сообщения об ошибке
                print(f"Database error: {e}")
            finally:
                await session.close()
    
    
db_helper = Database_Helper(url=SQLALCHEMY_DATABASE_URL)


