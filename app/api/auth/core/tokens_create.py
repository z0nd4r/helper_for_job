from app.api.auth.schemas import UserMain

from .utils import encode_jwt, decode_jwt

from .config import settings
def create_access_token(user: UserMain) -> str:
    jwt_payload = {
        'iss': 'crm_system_by_zondar',
        'type': 'access',
        'sub': user.id,
        'username': user.username,
        'email': user.email,
    }

    token = encode_jwt(
        payload=jwt_payload,
    )
    return token

def create_refresh_token(user: UserMain) -> str:
    jwt_payload = {
        'iss': 'crm_system_by_zondar',
        'type': 'refresh',
        'sub': user.id,
    }

    token = encode_jwt(
        payload=jwt_payload,
        expire_timedelta=settings.auth_jwt.refresh_token_expire_days,
    )
    return token