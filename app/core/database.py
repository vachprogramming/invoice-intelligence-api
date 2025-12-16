from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# 1. Create the Engine with strict settings
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
    # This dictionary is passed directly to asyncpg
    connect_args={
        "ssl": False,            # <--- Disable SSL (Fixing connection_lost)
        "server_settings": {
            "jit": "off"         # <--- Optimization for asyncpg
        }
    }
)

# 2. Creating the Session Factory
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# 3. The Base Class
Base = declarative_base()

# 4. Dependency Injection
async def get_db():
    async with SessionLocal() as session:
        yield session