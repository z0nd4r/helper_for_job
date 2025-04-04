from typing import List

from fastapi import Depends, APIRouter

from app.datadase.dependencies import get_db

from fastapi import HTTPException
from fastapi.templating import Jinja2Templates

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from app.datadase.models import Channel

from .schemas import ChannelCreate, ChannelUpdate, ChannelMain

router = APIRouter(prefix="/channels", tags=["Channels"])
tamplates = Jinja2Templates(directory="app/templates")

@router.get("/", response_model=List[ChannelMain], summary='Список каналов')
async def channels(
        db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Channel))
    channels_list = result.scalars().all()
    return channels_list

@router.get("/{channel_id}", response_model=ChannelMain, summary='Выбрать канал')
async def get_channel(
        channel_id: int,
        db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Channel).where(Channel.id == channel_id))
    channel = result.scalars().first()
    if not channel:
        raise HTTPException(status_code=404, detail="Канал не найден")
    return ChannelMain.model_validate(channel)

@router.post("/create_channel", response_model=ChannelMain, summary='Создать канал')
async def create_channel(
        channel: ChannelCreate,
        db: AsyncSession = Depends(get_db)
):
    db_channel = Channel(**channel.model_dump())
    db.add(db_channel)
    try:
        await db.commit()
        await db.refresh(db_channel)
        return ChannelMain.model_validate(db_channel)
    except IntegrityError as error:
        print(str(error))
        await db.rollback()
        if 'unique constraint "channels_name_key"' in str(error):
            raise HTTPException(
                status_code=400,
                detail="Такой канал уже существует"
            )
        else:
            raise HTTPException(status_code=500, detail="Ошибка при создании канала")

@router.put("/update_channel", response_model=ChannelMain, summary='Изменить канал')
async def update_channel(
        channel_id: int,
        channel_update: ChannelUpdate,
        db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Channel).where(Channel.id == channel_id))
    channel = result.scalars().first()
    if channel is None:
        raise HTTPException(status_code=404, detail='Канал не найден')
    for key, value in channel_update.model_dump().items():
        setattr(channel, key, value)
    db.add(channel)
    try:
        await db.commit()
        await db.refresh(channel)
        return channel
    except IntegrityError as error:
        await db.rollback()
        if 'unique constraint "channels_name_key"' in str(error):
            raise HTTPException(
                status_code=400,
                detail="Такой канал уже существует"
            )
        else:
            raise HTTPException(status_code=500, detail="Ошибка при изменении канала")

@router.delete("/{channel_id}", summary='Удалить канал')
async def delete_channel(
        channel_id: int,
        db: AsyncSession = Depends(get_db)
):
    try:
        result = await db.execute(select(Channel).where(Channel.id == channel_id))
        db_channel = result.scalars().first()
        if db_channel is None:
            raise HTTPException(status_code=404, detail='Канал не найден')
        await db.delete(db_channel)
        await db.commit()
        return {'message': 'Канал успешно удален'}
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=404, detail='Ошибка при удалении канала')
