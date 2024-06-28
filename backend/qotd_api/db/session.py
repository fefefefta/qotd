from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from config import get_settings


async_engine = create_async_engine(
    get_settings().database_uri,
    # echo=True,  # For debug
)

AsyncSessionFactory = sessionmaker(
    async_engine,
    expire_on_commit=False,
    class_=AsyncSession
)

# Generator for FastAPI Depends
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionFactory() as session:
        yield session
