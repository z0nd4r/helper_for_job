from pathlib import Path
from pydantic import BaseModel

# базовая директория, где находится весь проект
# resolve проверяет верен ли путь 
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent

class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / 'certs' / 'jwt-private.pem'
    public_key_path: Path = BASE_DIR / 'certs' / 'jwt-public.pem'
    algorithm: str = 'RS256'