from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.datadase.dependencies import get_db

from .schemas import UserReg, UserMain, UserLog

from app.api.auth import crud

router = APIRouter(prefix='/auth', tags = ['Auth'])

@router.post('/register', response_model=UserMain)
async def user_register(user: UserReg, db: AsyncSession = Depends(get_db)):
    return UserMain.model_validate(await crud.user_register(user, db))


@router.post('/login', response_model=UserMain)
async def user_login(user: UserLog, db: AsyncSession = Depends(get_db)):
    return UserMain.model_validate(await crud.user_login(user, db))

