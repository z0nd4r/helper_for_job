# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from sqlalchemy.orm import sessionmaker
#
# import asyncio
#
# from database import SQLALCHEMY_DATABASE_URL
#
# class DatabaseHelper:
#     def __init__(self, url: str):
#         self.engine = create_async_engine(
#             url=url,
#         )
#         self.session_factory = sessionmaker(
#             class_=AsyncSession,
#             bind=self.engine,
#             autoflush=False,
#             autocommit=False,
#             expire_on_commit=False,
#         )
#     async with self.engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#
#
# db_helper = Database_Helper(url=SQLALCHEMY_DATABASE_URL)


