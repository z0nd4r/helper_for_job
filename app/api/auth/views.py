from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.datadase.models import ClientAuth
from app.datadase.dependencies import get_db

from schemas import ClientReg, ClientMain

router = APIRouter(prefix='/auth', tags = ['Auth'])

security = HTTPBasic

@router.get('/test')
def test():
    return {'message:': 'Test'}

@router.post('/reg', response_model=ClientMain)
async def reg(client: ClientReg, db: AsyncSession = Depends(get_db)):
    db_client = ClientAuth(**client.model_dump())
    db.add(db_client)
    await db.commit()
    await db.refresh(db_client)
    return ClientMain.model_validate(db_client)

# @router.get('/auth_basic')
# def reg_basic(
#     credentials = Annotated[HTTPBasicCredentials, ]
# ):
#     pass

