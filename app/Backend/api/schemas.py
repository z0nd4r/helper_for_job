from pydantic import BaseModel, Field, PydanticUserError
from uuid import UUID
from typing import Optional

class TaskModel(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[bool] = None

class ItemCreate(TaskModel):
    pass

class ItemUpdate(TaskModel):
    pass


class Item_main(TaskModel):
    id: int

    class Config:
        from_attributes = True