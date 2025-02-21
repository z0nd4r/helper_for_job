from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasicCredentials

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from app.datadase.models import UserRegTablename
from app.datadase.dependencies import get_db

from .schemas import UserReg, UserMain, UserLog

from app.api.auth.core.utils import hash_password, validate_password


async def user_register(
        user: UserReg,
        db: AsyncSession = Depends(get_db)
):
    password = user.password  # получаем пароль
    hashed_password = hash_password(password)  # хэшируем пароль

    client_data = user.model_dump()  # получаем словарь из модели
    client_data['password'] = hashed_password  # заменяем пароль
    db_client = UserRegTablename(**client_data)
    db.add(db_client)
    try:
        await db.commit()
        await db.refresh(db_client)
        return db_client
    except IntegrityError as e:
        print(str(e))
        await db.rollback()
        if 'unique constraint "users_username_key"' in str(e):
            raise HTTPException(
                status_code=400,
                detail="Имя пользователя уже существует"
            )
        elif 'unique constraint "users_email_key"' in str(e):
            raise HTTPException(
                status_code=400,
                detail="Почта уже зарегистрирована"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error"
            )


async def user_login(
        user: UserLog,
        db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(UserRegTablename).where(user.email == UserRegTablename.email)
    )
    db_user = result.scalars().first()
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    password = user.password
    if not validate_password(password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return db_user