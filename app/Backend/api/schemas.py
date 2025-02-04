from pydantic import BaseModel, Field, PydanticUserError
from uuid import UUID

class TaskModel(BaseModel):
        id: UUID
        title: str = Field(max_length=30)
        description: str = Field(max_length=150)
        status: str