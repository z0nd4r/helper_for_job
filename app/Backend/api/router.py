from fastapi import APIRouter, HTTPException, Depends
from .schemas import TaskModel, Item_main, ItemCreate, ItemUpdate
from .models import Item
from .dependencies import get_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(prefix='/tasks')

@router.get('/all_tasks', response_model=List[Item_main], summary='Получить список задач')
def get_tasks(db: Session = Depends(get_db)):
    return db.query(Item).all()

@router.post('/add_task', response_model=Item_main, summary='Добавить задачу')
def add_tasks(task: ItemCreate, db: Session = Depends(get_db)):
    db_item = Item(**task.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.put('/tasks/{id}', response_model=Item_main, summary='Обновить задачу по id')
def update_task(id: int, item_update: ItemUpdate, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    for field, value in item_update.model_dump(exclude_unset=True).items():
        setattr(db_item, field, value)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete('/tasks/{id}', summary='Удалить задачу')
def delete_task(id: int, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    return {"message": "Item deleted successfully"}