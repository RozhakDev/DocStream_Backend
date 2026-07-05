import os

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "DocStream"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    APP_ENV: str = "development"

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    DATABASE_URL: str

    STORAGE_PATH: str = "./uploads"
    MAX_UPLOAD_SIZE: int = 52428800

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

settings = Settings()

os.makedirs(settings.STORAGE_PATH, exist_ok=True)