from fastapi import APIRouter, HTTPException, Depends
from .schemas import TaskModel, ClientMain, ClientCreate, ClientUpdate
from .models import Client
from .dependencies import get_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(prefix='/users')

@router.get('/all_users', response_model=List[ClientMain], summary='Получить список клиентов')
def get_tasks(db: Session = Depends(get_db)):
    return db.query(Client).all()

@router.post('/add_users', response_model=ClientMain, summary='Добавить клиента')
def add_tasks(task: ClientCreate, db: Session = Depends(get_db)):
    db_client = Client(**task.dict())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

@router.put('/users/{id}', response_model=ClientMain, summary='Изменить информацию о клиенте по id')
def update_task(id: int, item_update: ClientUpdate, db: Session = Depends(get_db)):
    db_client = db.query(Client).filter(Client.id == id).first()
    if db_client is None:
        raise HTTPException(status_code=404, detail="Item not found")
    for field, value in item_update.model_dump(exclude_unset=True).items():
        setattr(db_client, field, value)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

@router.delete('/users/{id}', summary='Удалить клиента')
def delete_task(id: int, db: Session = Depends(get_db)):
    db_client = db.query(Client).filter(Client.id == id).first()
    if db_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    db.delete(db_client)
    db.commit()
    return {"message": "Client deleted successfully"}