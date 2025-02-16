from fastapi import APIRouter, HTTPException, Depends

from app.datadase.models import Client
from app.datadase.dependencies import get_db

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from typing import List

from .schemas import ClientMain, ClientCreate, ClientUpdate


router = APIRouter(prefix='/users', tags=['Users'])

@router.get('/', response_model=List[ClientMain], summary='Получить список клиентов')
async def get_tasks(db: AsyncSession  = Depends(get_db)):
    result = await db.execute(select(Client))
    users = result.scalars().all()
    return users

# @router.get('/', response_model=List[ClientMain], summary='Получить список клиентов')
# async def get_tasks(db: AsyncSession  = Depends(get_db)):
#     return crud.get_tasks()

@router.post('/add_users/', response_model=ClientMain, summary='Добавить клиента')
async def add_tasks(task: ClientCreate, db: AsyncSession = Depends(get_db)):
    db_client = Client(**task.model_dump())
    db.add(db_client)
    await db.commit()
    await db.refresh(db_client)
    return ClientMain.model_validate(db_client)

# @router.post('/add_users/', response_model=ClientMain, summary='Добавить клиента')
# async def add_users(user: ClientCreate, db: AsyncSession = Depends(get_db)):
#     return crud.add_users(user=user)

@router.put('/{id}/', response_model=ClientMain, summary='Изменить информацию о клиенте по id')
async def update_task(id: int, item_update: ClientUpdate, db: AsyncSession  = Depends(get_db)):
    result = await db.execute(select(Client).where(Client.id == id))
    db_client = result.scalars().first()
    if db_client is None:
        raise HTTPException(status_code=404, detail="Item not found")
    for field, value in item_update.model_dump(exclude_unset=True).items():
        setattr(db_client, field, value)
    db.add(db_client)
    await db.commit()
    await db.refresh(db_client)
    return ClientMain.model_validate(db_client)

@router.delete('/{id}/', summary='Удалить клиента')
async def delete_task(id: int, db: AsyncSession  = Depends(get_db)):
    result = await db.execute(select(Client).where(Client.id == id))
    db_client = result.scalars().first()
    if db_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    await db.delete(db_client)
    await db.commit()
    return {"message": "Client deleted successfully"}