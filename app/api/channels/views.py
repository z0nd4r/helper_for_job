from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from typing import List

from app.datadase.dependencies import get_db

from .schemas import ChannelSchema, ChannelCreate, ChannelMain, ChannelUpdate

from app.api.channels import crud

router = APIRouter(prefix="/channels", tags=["Channels"])

@router.get("/", response_model=List[ChannelMain], summary='Список каналов')
async def channels(
        db: AsyncSession = Depends(get_db)
):
    return await crud.get_channels(db)

@router.get("/{channel_id}", response_model=ChannelMain, summary='Выбрать канал')
async def get_channel(
        channel_id: int,
        db: AsyncSession = Depends(get_db)
):
    return ChannelMain.model_validate(await crud.get_channel(channel_id, db))


@router.post("/create_channel", response_model=ChannelMain, summary='Создать канал')
async def create_channel(
        channel: ChannelCreate,
        db: AsyncSession = Depends(get_db)
):
    return ChannelMain.model_validate(await crud.create_channel(channel, db))

@router.put("/update_channel", response_model=ChannelMain, summary='Изменить канал')
async def update_channel(
        channel_id: int,
        channel_update: ChannelUpdate,
        db: AsyncSession = Depends(get_db)
):
    return await crud.update_channel(channel_id, channel_update, db)

@router.delete("/{channel_id}", summary='Удалить канал')
async def delete_channel(
        channel_id: int,
        db: AsyncSession = Depends(get_db)
):
    return await crud.delete_channel(channel_id, db)
