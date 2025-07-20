from typing import List

from fastapi import APIRouter, Depends, Cookie, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.templating import Jinja2Templates

from .schemas import FriendSchema
from api.auth.core.utils import access_token_validate
from database import get_db, Friend, UserRegTablename

router = APIRouter(
    prefix="/friends",
    tags=["friends"],
)
tamplates = Jinja2Templates(directory="app/templates")


@router.get('/', response_model=List[FriendSchema], summary="Список друзей")
async def get_friends(
    access_token: str = Cookie(None, alias='access_token'),
    db: AsyncSession = Depends(get_db)
):
    payload = access_token_validate(access_token)

    result = await db.execute(select(Friend).where(Friend.user_id == payload.get('user_id')))
    friends_list = result.scalars().all()
    return friends_list


@router.get('/{friend_id}', response_model=FriendSchema, summary='Информация о друге')
async def get_friend(
    friend_id: int,
    access_token: str = Cookie(None, alias='access_token'),
    db: AsyncSession = Depends(get_db),
):
    payload = access_token_validate(access_token)

    result = await db.execute(select(Friend).where(Friend.user_id == payload.get('user_id')))
    friends_list = result.scalars().all()

    for d in friends_list:
        data = d.__dict__ # получаем словарь из SQLAlchemy объекта
        if data['friend_id'] == friend_id:
            print(d)
            return d


@router.post('/add_friend', summary='Добавить друга по нику')
async def add_friend(
    username: str,
    access_token: str = Cookie(None, alias='access_token'),
    db: AsyncSession = Depends(get_db),
):
    payload = access_token_validate(access_token)

    # пользователь, КОТОРОГО ДОБАВЛЯЮТ в друзья
    result = await db.execute(select(UserRegTablename).where(UserRegTablename.username == username))
    friend_sql_data = result.scalars().first()
    if friend_sql_data is None:
        raise HTTPException(status_code=404, detail='Пользователь не найден')
    friend = friend_sql_data.__dict__

    db_friend = Friend(
        user_id=payload.get('user_id'), # пользователь, КОТОРЫЙ ДОБАВЛЯЕТ в друзья
        friend_id=friend['id'], # пользователь, КОТОРОГО ДОБАВЛЯЮТ в друзья
        friend_name=friend['username']
    )
    db.add(db_friend)
    try:
        await db.commit()
        await db.refresh(db_friend)
        return db_friend
    except IntegrityError as error:
        print(str(error))
        await db.rollback()
        raise HTTPException(status_code=500, detail="Ошибка при добавлении пользователя в друзья")

@router.delete('/{friend_id}', summary='Удалить пользователя из списка друзей')
async def delete_friend(
        friend_id: int,
        access_token: str = Cookie(None, alias='access_token'),
        db: AsyncSession = Depends(get_db),
):
    payload = access_token_validate(access_token)

    try:
        # список друзей именно авторизованного пользователя
        result = await db.execute(select(Friend).where(Friend.user_id == payload.get('user_id')))
        friends_list = result.scalars().all()
        print('Отчет 1')

        # пользователь, КОТОРОГО УДАЛЯЮТ из друзей
        friend_main = None

        print('Отчет 2')
        for d in friends_list:
            data = d.__dict__  # получаем словарь из SQLAlchemy объекта
            if data['friend_id'] == friend_id:
                friend_main = data

                print('Отчет 3')
        if friend_main is None:
            raise HTTPException(status_code=404, detail='Пользователь не найден')

        print('Отчет 4')
        result = await db.execute(select(Friend).where(Friend.id == friend_main['id']))
        db_friend = result.scalars().first()
        await db.delete(db_friend)
        await db.commit()
        return {'message': 'Пользователь удален из списка друзей'}
    except:
        await db.rollback()
        raise HTTPException(status_code=404, detail='Ошибка при удалении пользователя')