from fastapi import APIRouter, HTTPException, Depends
from .schemas import ClientMain, ClientCreate, ClientUpdate
from ...datadase.models import Client
from ...datadase.db_helper import get_session
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(prefix='/users', tags=['Users'])

@router.get('/', response_model=List[ClientMain], summary='Получить список клиентов')
async def get_tasks(db: Session = Depends(get_session)):
    return await db.query(Client).all()

@router.post('/add_users/', response_model=ClientMain, summary='Добавить клиента')
async def add_tasks(task: ClientCreate, db: Session = Depends(get_session)):
    db_client = Client(**task.model_dump())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return await db_client

@router.put('/{id}/', response_model=ClientMain, summary='Изменить информацию о клиенте по id')
async def update_task(id: int, item_update: ClientUpdate, db: Session = Depends(get_session)):
    db_client = db.query(Client).filter(Client.id == id).first()
    if db_client is None:
        raise HTTPException(status_code=404, detail="Item not found")
    for field, value in item_update.model_dump(exclude_unset=True).items():
        setattr(db_client, field, value)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return await db_client

@router.delete('/{id}/', summary='Удалить клиента')
async def delete_task(id: int, db: Session = Depends(get_session)):
    db_client = db.query(Client).filter(Client.id == id).first()
    if db_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    db.delete(db_client)
    db.commit()
    return await {"message": "Client deleted successfully"}