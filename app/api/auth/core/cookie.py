from datetime import timedelta, datetime, timezone
from email.utils import format_datetime

from fastapi import Response


def add_access_with_refresh_tokens_to_cookie(response: Response, access_token, refresh_token):
    # expires_time = datetime.utcnow() + timedelta(days=7)
    # expires_seconds = int(expires_time.timestamp())  # Unix timestamp

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True, # запрещает доступ JavaScript к cookie
        # secure=True,  # только для HTTPS
        samesite=None,  # Или "strict" или 'lax' для более строгой защиты
        max_age=int(timedelta(days=7).total_seconds()),  # срок действия в секундах
        path="/"  # cookie действителен для всего домена
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,  # запрещает доступ JavaScript к cookie
        # secure=True,  # только для HTTPS
        samesite=None,  # Или "strict" для более строгой защиты
        max_age=int(timedelta(days=7).total_seconds()),  # срок действия в секундах с эпохи
        path="/"  # cookie действителен для всего домена
    )


def delete_cookie_helper(response: Response, cookie_name: str):
    expires = datetime.now(timezone.utc) - timedelta(seconds=1) # Получаем текущее UTC-время
    print(f'Name_func: delete_cookie_helper (cookie.py). Info: name_cookie: {cookie_name}')
    response.set_cookie(
        key=cookie_name,
        value="",  # Устанавливаем пустое значение
        httponly=True,
        # secure=True,  # Раскомментируйте, если использовали Secure=True при установке
        samesite=None,  # Или "strict", если использовали
        # max_age=0,  # Устанавливаем срок действия в 0 секунд (в прошлом)
        expires=format_datetime(expires, usegmt=True),
        path="/",  # Убедитесь, что путь совпадает с путем при установке куки
        domain="127.0.0.1"
    )


