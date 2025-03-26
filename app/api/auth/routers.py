import logging
import sys
from typing import Annotated, Union

from fastapi import Depends, HTTPException, status, Form, APIRouter, Cookie, Response
from fastapi.security import HTTPBearer, OAuth2PasswordBearer, OAuth2PasswordRequestForm

from jwt.exceptions import InvalidTokenError

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from app.datadase.models import UserRegTablename
from app.datadase.dependencies import get_db
from .core.cookie import add_access_with_refresh_tokens_to_cookie

from .schemas import UserReg, UserMain, TokenInfo

from app.api.auth.core.utils import hash_password, validate_password, decode_jwt

from .core.tokens_create import create_access_token, create_refresh_token

# настройка базовой конфигурации логирования
logging.basicConfig(
    level=logging.DEBUG,  # уровень логирования DEBUG
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)  # отправляем логи в консоль
    ]
)

logger = logging.getLogger(__name__)

http_bearer = HTTPBearer(auto_error=False)
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='/auth/login',
)
router = APIRouter(
    prefix='/auth',
    tags=['Auth'],
    dependencies=[Depends(http_bearer)],
)


@router.post('/register', response_model=UserMain, summary='Регистрация пользователя')
async def user_register(
        user: Annotated[UserReg, Form()],
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
        return UserMain.model_validate(db_client)
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


@router.post('/login',
             # response_model=Union[UserMain, TokenInfo],
             summary='Авторизация пользователя'
             )
async def user_login(
        # user: Annotated[UserLog, Form()],
        response: Response,
        user_data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(get_db)
):
    logger.debug(f"Received user {user_data}")
    logger.debug(f'Received user {user_data.username}, {user_data.password}')

    result = await db.execute(
        select(UserRegTablename).where(user_data.username == UserRegTablename.email)
    )
    db_user = result.scalars().first()
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    password = user_data.password
    if not validate_password(password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(db_user)
    refresh_token = create_refresh_token(db_user)

    add_access_with_refresh_tokens_to_cookie(response, access_token, refresh_token)

    return {'message': 'Authorization successful'}
    # return TokenInfo(
    #     access_token=access_token,
    #     refresh_token=refresh_token,
    # )

@router.post('/refresh',
             # response_model=TokenInfo,
             response_model_exclude_none=True,
             summary='Выпуск нового access токена'
             )
async def auth_refresh_jwt(
    # refresh_token: str = Depends(oauth2_scheme), # получаем токен напрямую
    response: Response,
    refresh_token: str = Cookie(None, alias='refresh_token'),
    db: AsyncSession = Depends(get_db),
):
    try:
        # декодируем токен и получаем полезную нагрузку (в виде словаря)
        payload = decode_jwt(
            token=refresh_token,
        )
        token_type = payload.get('type')
        # проверяем тип токена
        if token_type != 'refresh':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"invalid token type {token_type!r} expected 'refresh'"
            )
    except InvalidTokenError as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='token invalid error'
        )

    result = await db.execute(select(UserRegTablename).where(UserRegTablename.username == payload.get('sub')))
    db_user = result.scalars().first()
    print(payload)
    print(db_user)

    access_token = create_access_token(db_user)

    add_access_with_refresh_tokens_to_cookie(response, access_token, refresh_token)

    return {'message': 'ok'}
    # return TokenInfo(
    #     access_token=access_token,
    # )

@router.get('/users/me', response_model=UserMain, summary='Get user info')
async def auth_user_check_self_info(
    # credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    # token: str = Depends(oauth2_scheme), # получаем токен напрямую
    access_token: str = Cookie(None, alias='access_token'),
    db: AsyncSession = Depends(get_db),
) -> UserMain:
    # получаем токен в виде строки
    # token = credentials.credentials

    try:
        # декодируем токен и получаем полезную нагрузку (в виде словаря)
        payload = decode_jwt(
            token=access_token,
        )
        token_type = payload.get('type')
        # проверяем тип токена
        if token_type != 'access':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"invalid token type {token_type!r} expected 'access'"
            )
    except InvalidTokenError as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='token invalid error'
        )
    result = await db.execute(select(UserRegTablename).where(UserRegTablename.email == payload.get('email')))
    db_user = result.scalars().first()
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='user no found (token invalid)'
        )
    return UserMain.model_validate(db_user)
