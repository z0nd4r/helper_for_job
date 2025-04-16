from pydantic import BaseModel, EmailStr, ConfigDict

class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = 'Bearer'

class UserReg(BaseModel):
    model_config = ConfigDict(strict = True)

    username: str
    password: str
    email: EmailStr 


class UserLog(BaseModel):
    # model_config = ConfigDict(strict = True)

    username: EmailStr
    password: str


class UserMain(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True

class CookieName(BaseModel):
    cookie_name: str

class UserInfo(BaseModel):
    username: str
    email: EmailStr