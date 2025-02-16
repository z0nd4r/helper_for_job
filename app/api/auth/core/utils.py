import jwt 
import bcrypt

from .config import AuthJWT

# шифруем токен
def encode_jwt(
    payload: dict,
    private_key: str = AuthJWT.private_key_path.read_text(),
    algorithm: str = AuthJWT.algorithm,
) -> str:
    
    encoded = jwt.encode(
        payload,
        private_key,
        algorithm=algorithm,
    )
    return encoded


# расшифровываем токен
def decode_jwt(
    token: str | bytes,
    public_key: str = AuthJWT.public_key_path.read_text(),
    algorithm: str = AuthJWT.algorithm,
) -> dict:
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm],
    )
    return decoded

# шифруем пароль
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