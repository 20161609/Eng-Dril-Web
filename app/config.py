from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, EmailStr
from typing import Optional

class Settings(BaseSettings):
    APP_NAME: str = "Eng-Drill"
    ENV: str = "production"

    SECRET_KEY: str = "please-change-me-32chars-min"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    DATABASE_URL: str = "sqlite:///./engdrill.db"

    CORS_ORIGINS: str = "*"

    # Email
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASS: Optional[str] = None
    SMTP_FROM: Optional[str] = None

    PUBLIC_API_BASE: Optional[AnyHttpUrl] = None

    MODEL_API_BASE: str = "https://qe-api-487754022529.northamerica-northeast1.run.app"
    MODEL_API_KEY: Optional[str] = None

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()