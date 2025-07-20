from api.auth.schemas import UserMain

from .utils import encode_jwt

from .config import settings

def create_access_token(user: UserMain) -> str:
    jwt_payload = {
        'iss': 'crm_system_by_zondar',
        'type': 'access',
        'sub': user.username,
        'user_id': user.id,
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
        'sub': user.username,
    }

    token = encode_jwt(
        payload=jwt_payload,
        expire_timedelta=settings.auth_jwt.refresh_token_expire_days,
    )
    return token