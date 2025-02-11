from pydantic import BaseModel, EmailStr
from typing import Optional

class TaskModel(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None

class ClientCreate(TaskModel):
    pass

class ClientUpdate(TaskModel):
    pass

class ClientMain(TaskModel):
    id: int

    class Config:
        from_attributes = True