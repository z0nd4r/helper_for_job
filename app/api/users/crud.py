# from fastapi import APIRouter, HTTPException, Depends

# from .schemas import ClientMain, ClientCreate, ClientUpdate

# from app.Backend.datadase.models import Client
# from app.Backend.datadase.dependencies import get_db

# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy import select

# from typing import List

# async def add_users(user: ClientCreate, db: AsyncSession = Depends(get_db)):
#     db_client = Client(**user.model_dump())
#     db.add(db_client)
#     await db.commit()
#     await db.refresh(db_client)
#     return ClientMain.model_validate(db_client)

# # async def get_tasks(db: AsyncSession  = Depends(get_db)):
# #     result = await db.execute(select(Client))
# #     users = result.scalars().all()
# #     return users
