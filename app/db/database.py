from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

from app.core.config import settings
from app.scripts.load_data import load_csv_to_db
from app.db.base import Base

engine = create_async_engine(settings.ASYNC_DATABASE_URL)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession)


async def init_db():
    """Создает таблицы в базе данных"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session():
    """Генерирует асинхронную сессию для работы с БД"""
    async with async_session_maker() as session:
        yield session


async def load_initial_data():
    """Загружает начальные данные в БД из CSV"""
    async with async_session_maker() as session:
        await load_csv_to_db(session)
        await session.commit()