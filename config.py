from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_PATH = os.path.join(BASE_DIR, "storage")


class Settings(BaseSettings):
    
    db_login: str = 'postgres'
    db_password: str
    db_name: str
    db_host: str
    db_port: str
    aes_key: str
    jwt_secret_key: str
    jwt_algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_minutes: int

    current_host: str
    openai_api_key: str
    fixed_IV: bytes = Field(default=b"\x00" * 16)
    admin_user_login: str
    admin_user_password: str

    broker_host: str

    class Me:
        scheme: str = "http"
        host: str = "0.0.0.0"
        port: int = 8007
        title: str = "Test backend"
        apis: list[str] = []
        deps: list[str] = []

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache()
def get_settings() -> Settings:
    return Settings()
