from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

class ClientReg(BaseModel):
    model_config = ConfigDict(strict = True)

    username: str
    password: bytes
    email: EmailStr | None = None
    active: bool = True


class ClientMain(ClientReg):
    id: int

    class Config:
        from_attributes = True