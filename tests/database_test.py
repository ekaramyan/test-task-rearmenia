from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import get_settings
from sqlalchemy.ext.asyncio import AsyncSession

settings = get_settings()
driver_path = f"postgresql+asyncpg://{settings.test_db_login}:{settings.test_db_password}@{settings.test_db_host}/{settings.test_db_name}"  # noqa 501

engine = create_async_engine(url=driver_path)

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
