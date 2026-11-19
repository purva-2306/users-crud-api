
import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)

load_dotenv()

raw_database_url = os.getenv("DATABASE_URL")

if not raw_database_url:
    raise ValueError("DATABASE_URL is missing from .env file")

# Convert PostgreSQL URL to asyncpg format
DATABASE_URL = raw_database_url.replace(
    "postgresql+psycopg2://",
    "postgresql+asyncpg://",
    1
).replace(
    "postgresql://",
    "postgresql+asyncpg://",
    1
).replace(
    "postgres://",
    "postgresql+asyncpg://",
    1
)

# Async PostgreSQL engine
async_engine = create_async_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

# Async database session
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)


# Async database dependency
async def get_async_db():
    async with AsyncSessionLocal() as db:
        yield db