from fastapi import APIRouter
from app.Backend.api.schemas import TaskModel

router = APIRouter(prefix='/tasks')

@router.get('/all_tasks', summary='Получить список задач')
def get_tasks(task: TaskModel):
    return {id: task.id,
            title: task.title,
            description: task.description,
            status: task.status}

@router.post('/add_task', summary='Добавить задачу')
def add_tasks(task: TaskModel):
    return {id: task.id,
            title: task.title,
            description: task.description,
            status: task.status}

@router.put('/tasks/{id}', summary='Обновить задачу по id')
def update_task(id: int):
    return {id: id}

@router.delete('/tasks/{id}', summary='Удалить задачу')
def delete_task(id: int):
    return {id: id}