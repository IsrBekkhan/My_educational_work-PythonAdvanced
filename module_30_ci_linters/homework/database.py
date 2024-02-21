from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

DATABASE_URL = "sqlite+aiosqlite:///./cookbook.db"

async_engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(async_engine, expire_on_commit=False)

session = async_session()
Base = declarative_base()
