from pydantic import BaseModel, EmailStr
from typing import Optional

class ClientReg(BaseModel):
    email: Optional[EmailStr] = None
    password: str