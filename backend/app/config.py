# tms_system/app/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://tmsdb_zvjr_user:4FQNkYhbcS4UEPzUv8OaIwOL2DVRt47o@dpg-cug6pqqj1k6c738jermg-a/tmsdb_zvjr"
    SECRET_KEY: str = "tu_clave_secreta_muy_segura"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings():
    return Settings()

