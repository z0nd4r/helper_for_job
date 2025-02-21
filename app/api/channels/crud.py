from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from app.datadase.models import Channel

from .schemas import ChannelSchema, ChannelCreate, ChannelMain, ChannelUpdate



async def get_channels(db: AsyncSession):
    result = await db.execute(select(Channel))
    channels = result.scalars().all()
    return channels


async def get_channel(
        channel_id: int,
        db: AsyncSession
):
    result = await db.execute(select(Channel).where(Channel.id == channel_id))
    channel = result.scalars().first()
    if not channel:
        raise HTTPException(status_code=404, detail="Канал не найден")
    return channel


async def create_channel(
        channel: ChannelCreate,
        db: AsyncSession
):
    db_channel = Channel(**channel.model_dump())
    db.add(db_channel)
    try:
        await db.commit()
        await db.refresh(db_channel)
        return db_channel
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


async def update_channel(
        channel_id: int,
        channel_update: ChannelUpdate,
        db: AsyncSession
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

async def delete_channel(
        channel_id: int,
        db: AsyncSession
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
