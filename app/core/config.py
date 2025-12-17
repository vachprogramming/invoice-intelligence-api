from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # 1. Give these DEFAULTS so they are not "Required" anymore
    POSTGRES_USER: str = "admin"
    POSTGRES_PASSWORD: str = "admin"
    POSTGRES_DB: str = "invoice_db"
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    
    # 2. Render gives us this one
    DATABASE_URL: Optional[str] = None
    HUGGINGFACE_API_KEY: Optional[str] = None

    @property
    def FINAL_DATABASE_URL(self) -> str:

        if self.DATABASE_URL:
            # Fix 1: Protocol
            url = self.DATABASE_URL.replace("postgres://", "postgresql+asyncpg://")
            # Fix 2: SSL for Neon
            if "?" not in url:
                url += "?ssl=require"
            return url
            
        # Otherwise (Localhost), build from the parts
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()