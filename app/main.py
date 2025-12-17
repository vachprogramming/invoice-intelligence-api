from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.database import engine, Base

from app.models import invoice 

from app.api.endpoints import invoices

# 1. Defining what happens when the app starts
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables
    print("Creating tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown: (Nothing to do yet)

app = FastAPI(
    title="Invoice Intelligence API",
    version="0.2.0",
    lifespan=lifespan # Connect the lifespan logic
)

# Connect the router
app.include_router(invoices.router, prefix="/api/v1", tags=["invoices"])

@app.get("/")
def read_root():
    return {"status": "online", "db": "connected"}