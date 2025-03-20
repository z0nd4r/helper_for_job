from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings

# базовая директория, где находится весь проект
# resolve проверяет верен ли путь 
BASE_DIR = Path(__file__).parent.parent.parent.parent.parent

class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / 'certs' / 'jwt-private.pem'
    public_key_path: Path = BASE_DIR / 'certs' / 'jwt-public.pem'
    algorithm: str = 'RS256'
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30


class Settings(BaseSettings):
    auth_jwt: AuthJWT = AuthJWT()

settings = Settings()