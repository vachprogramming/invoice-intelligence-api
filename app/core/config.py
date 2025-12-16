from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # These match the variable names in your .env file
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: int

    # This constructs the full connection URL automatically
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    class Config:
        env_file = ".env"

# Create a single instance to use everywhere
settings = Settings()