
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Load environment variables from .env
load_dotenv()

# Get PostgreSQL connection URL
raw_database_url = os.getenv("DATABASE_URL")

if not raw_database_url:
    raise ValueError("DATABASE_URL is missing from .env file")

# Convert PostgreSQL URL for psycopg2
DATABASE_URL = raw_database_url.replace(
    "postgresql://",
    "postgresql+psycopg2://",
    1
)

# Create PostgreSQL engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

# Create database session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for database models
class Base(DeclarativeBase):
    pass


# Database connection dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()