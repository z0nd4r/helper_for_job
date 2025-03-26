from datetime import timedelta, datetime
from fastapi import Response


def add_access_with_refresh_tokens_to_cookie(response: Response, access_token, refresh_token):
    expires_time = datetime.utcnow() + timedelta(days=7)
    expires_seconds = int(expires_time.timestamp())  # Unix timestamp

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True, # запрещает доступ JavaScript к cookie
        secure=True,  # только для HTTPS
        samesite="lax",  # Или "strict" для более строгой защиты
        expires=expires_seconds,  # срок действия в секундах с эпохи
        path="/"  # cookie действителен для всего домена
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,  # запрещает доступ JavaScript к cookie
        secure=True,  # только для HTTPS
        samesite="lax",  # Или "strict" для более строгой защиты
        expires=expires_seconds,  # срок действия в секундах с эпохи
        path="/"  # cookie действителен для всего домена
    )

