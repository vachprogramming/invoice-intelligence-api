from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    POSTGRES_USER: str = "admin"
    POSTGRES_PASSWORD: str = "admin"
    POSTGRES_DB: str = "invoice_db"
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    
    # Render/Neon gives us this string
    DATABASE_URL: Optional[str] = None
    HUGGINGFACE_API_KEY: Optional[str] = None

    @property
    def FINAL_DATABASE_URL(self) -> str:
        if self.DATABASE_URL:
            url = self.DATABASE_URL
            
            # This handles "postgres://", "postgresql://", etc.
            if "postgresql+asyncpg://" not in url:

                url = "postgresql+asyncpg://" + url.split("://", 1)[1]
            
            # Ensuring SSL is enabled (Required for Neon)
            if "ssl=require" not in url:
                if "?" in url:
                    url += "&ssl=require"
                else:
                    url += "?ssl=require"
                    
            return url
            
        # Localhost fallback
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()