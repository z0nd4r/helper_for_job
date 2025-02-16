from .database import AsyncSessionLocal


async def get_db(): #создать сессию базы данных и закрыть ее после завершения запроса
    async with AsyncSessionLocal() as session:
        try:
            yield session #вернуть сессию базы данных которая будет использоваться в запросе
        finally:
            await session.close() #закрыть сессию




 