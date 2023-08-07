from typing import AsyncIterator

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

connection_string = "postgresql+asyncpg://user_name:user_password@first_app_postgres:5432/postgres"

async_engine = create_async_engine(
    connection_string,
    echo=False,
    pool_size=10,
    max_overflow=0,
    future=True,
)
async_session = async_sessionmaker(
    bind=async_engine,
    autoflush=False,
    future=True,
)
metadata = MetaData()
Base = declarative_base(metadata=metadata)


async def get_db() -> AsyncIterator[AsyncSession]:
    db = async_session()
    try:
        yield db
    finally:
        await db.close()
