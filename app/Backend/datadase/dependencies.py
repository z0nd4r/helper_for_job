from .database import AsyncSessionLocal

# async def get_db(): #создать сессию базы данных и закрыть ее после завершения запроса
#     async with
#     db = SessionLocal()
#     try:
#         yield db #вернуть сессию базы данных которая будет использоваться в запросе
#     finally:
#         await db.close() #закрыть сессию
#
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()



 