import logging
import sys
from typing import Annotated

from fastapi import Depends, HTTPException, status, Form, APIRouter, Cookie, Response
from fastapi.security import HTTPBearer, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates

from jwt.exceptions import InvalidTokenError

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from app.datadase.models import UserRegTablename, RefreshTokens
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
tamplates = Jinja2Templates(directory="app/templates")


@router.post('/register', summary='Регистрация пользователя')
async def user_register(
        response: Response,
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
        # return UserMain.model_validate(db_client)
    except IntegrityError as e:
        print(str(e))
        await db.rollback()
        if 'unique constraint "users_username_key"' in str(e):
            raise HTTPException(
                status_code=400,
                detail={'message': "Имя пользователя уже существует"}
            )
        elif 'unique constraint "users_email_key"' in str(e):
            raise HTTPException(
                status_code=400,
                detail={'message': "Почта уже зарегистрирована"}
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={'message': "Ошибка получения данных"}
            )

    result = await db.execute(select(UserRegTablename).where(UserRegTablename.email == user.email))
    db_user = result.scalars().first()

    access_token = create_access_token(db_user)
    refresh_token = create_refresh_token(db_user)

    dict_refresh_token = {
        'user_id': db_user.id,
        'token': refresh_token,
    }

    db_refresh_token = RefreshTokens(**dict_refresh_token)
    db.add(db_refresh_token)
    await db.commit()
    await db.refresh(db_refresh_token)

    add_access_with_refresh_tokens_to_cookie(response, access_token, refresh_token)

    return {'message': 'Registation successful'}


@router.post('/login',
             response_model=TokenInfo,
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
    try:
        result = await db.execute(
            select(UserRegTablename).where(user_data.username == UserRegTablename.email)
        )
        db_user = result.scalars().first()
        if db_user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                # detail={'message': 'Incorrect email or password'},
                detail={'message': 'Неправильная почта или пароль'},
                headers={"WWW-Authenticate": "Bearer"},
            )
        password = user_data.password
        if not validate_password(password, db_user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                # detail={'message': 'Incorrect email or password'},
                detail={'message': 'Неправильная почта или пароль'},
                headers={"WWW-Authenticate": "Bearer"},
            )
        if user_data.username == '' or user_data.password == '':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                # detail={'message': 'Email or password is empty'},
                detail={'message': 'Неправильная почта или пароль'},
            )
    except HTTPException as e:
        raise e  # Повторно выбрасываем исключение, чтобы оно было обработано FastAPI
    except Exception as e:
        print(f"Unexpected error: {e}")  # Логируем неожиданные ошибки
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            # detail={"message": "Internal server error"}
            detail={"message": "Ошибка сервера"}
        )

    access_token = create_access_token(db_user)
    refresh_token = create_refresh_token(db_user)

    try:
        # получаем старый рефреш токен из бд
        result = await db.execute(select(RefreshTokens).where(RefreshTokens.user_id == db_user.id))
        refresh_token_db = result.scalars().first()

        # если он есть, то меняем его на новый и добавляем в бд
        if refresh_token_db:
            refresh_token_db.token = refresh_token
            db.add(refresh_token_db)
            await db.commit()
            await db.refresh(refresh_token_db)
        else:
            dict_refresh_token = {
                'user_id': db_user.id,
                'token': refresh_token,
            }

            refresh_token_db = RefreshTokens(**dict_refresh_token)
            db.add(refresh_token_db)
            await db.commit()
            await db.refresh(refresh_token_db)

    except Exception as e:
        print(f"Ошибка: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            # detail={"message": "Internal server error"}
            detail={"message": "Ошибка сервера"}
        )

    add_access_with_refresh_tokens_to_cookie(response, access_token, refresh_token)

    # return {'message': 'Authorization successful'}
    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
    )

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

    # выбрать пользователя, которому присваивается токен
    result = await db.execute(select(UserRegTablename).where(UserRegTablename.username == payload.get('sub')))
    db_user = result.scalars().first()
    print(payload)
    print(db_user)

    # получаем новые токены
    access_token = create_access_token(db_user)
    refresh_token = create_refresh_token(db_user)

    # для замены токена в бд
    dict_refresh_token = {
        'user_id': db_user.id, # id для связи двух таблиц, юзеров и токенов
        'token': refresh_token,
    }

    # получаем строку со старым токеном из таблицы с токенами
    result = await db.execute(select(RefreshTokens).where(RefreshTokens.user_id == db_user.id))
    refresh_token_db = result.scalars().first()

    # меняем старый рефреш токен из бд на новый
    for key, value in dict_refresh_token.items():
        setattr(refresh_token_db, key, value)

    # добавляем новый токен в бд
    print('refresh', refresh_token_db)

    db.add(refresh_token_db)
    await db.commit()
    await db.refresh(refresh_token_db)

    # положить токены в куки
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
