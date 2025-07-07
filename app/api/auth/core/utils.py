import uuid

import jwt
import bcrypt

from fastapi import HTTPException, status
from datetime import datetime, timedelta

from jwt import InvalidTokenError

from .config import settings


# шифруем токен
def encode_jwt(
    payload: dict,
    private_key: str = settings.auth_jwt.private_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
) -> str:

    to_encode = payload.copy()

    now = datetime.utcnow()
    if expire_timedelta:
        expire = now + timedelta(days=expire_timedelta)
    else:
        expire = now + timedelta(minutes=expire_minutes)

    to_encode.update(
        jti=str(uuid.uuid4()),
        iat=now,
        exp=expire,

    )

    encoded = jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm,
    )
    return encoded


# расшифровываем токен
def decode_jwt(
    token: str | bytes,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
) -> dict:
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm],
    )
    return decoded

# проверка на правильность токена
def access_token_validate(access_token):
    try:
        # декодируем токен и получаем полезную нагрузку (в виде словаря)
        payload = decode_jwt(
            token=access_token
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
    return payload

# хэшируем пароль
def hash_password(
    password: str
) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)

# проверить совпадение пароля с хэшированным
def validate_password(
    password: str,
    hashed_password: bytes,
) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password,
    )
