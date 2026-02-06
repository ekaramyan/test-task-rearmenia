from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import get_settings
from sqlalchemy.ext.asyncio import AsyncSession


settings = get_settings()
driver_path: str = f"postgresql+asyncpg://{settings.db_login}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"  # noqa 501

engine = create_async_engine(
    url=driver_path,
    pool_pre_ping=True,
    pool_size=20,
    max_overflow=0)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False)
Base = declarative_base()


async def get_async_db() -> AsyncSession:
    async with AsyncSessionLocal() as async_session:
        try:
            yield async_session
        finally:
            await async_session.close()
