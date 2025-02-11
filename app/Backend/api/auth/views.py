from fastapi import APIRouter, Body
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Annotated
from pydantic import EmailStr

router = APIRouter(prefix='/auth', tags = ['Auth'])

security = HTTPBasic

@router.get('/test')
def test():
    return {'message:': 'Test'}

@router.post('/reg')
def reg(email: EmailStr = Body()):
    return {
        'message': 'success',
        'email': email
    }

# @router.get('/auth_basic')
# def reg_basic(
#     credentials = Annotated[HTTPBasicCredentials, ]
# ):
#     pass

