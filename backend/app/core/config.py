from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/factursaas"
    CLERK_SECRET_KEY: Optional[str] = None
    CLERK_WEBHOOK_SIGNING_SECRET: Optional[str] = None
    
    class Config:
        env_file = ".env"

settings = Settings()