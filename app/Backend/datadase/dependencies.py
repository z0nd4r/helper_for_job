# from .database import SessionLocal

# async def get_db(): #создать сессию базы данных и закрыть ее после завершения запроса
#     async with 
#     db = SessionLocal()
#     try:
#         yield db #вернуть сессию базы данных которая будет использоваться в запросе
#     finally:
#         await db.close() #закрыть сессию

import asyncio
from sqlalchemy.future import select
from .db_helper import db_helper

async def example_usage():
    async for session in db_helper.get_session():
        # Выполнение асинхронного запроса с использованием сессии
        try:
            result = await session.execute(select(SomeModel))
            data = result.scalars().all()
            print(data)
        except Exception as e:
            print(f"An error occurred: {e}")

# Запуск примера
asyncio.run(example_usage())

 