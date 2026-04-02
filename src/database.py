from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from src.config import settings

engine = create_async_engine(
    settings.DB_URL,
    echo=True,                # для отладки SQL-запросов и ошибок
    pool_pre_ping=True,       # проверять соединение перед использованием
    pool_size=5,              # размер пула
    max_overflow=10,          # дополнительных соединений при перегрузке
    pool_recycle=3600         # пересоздавать соединения раз в час
)

async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

class Base(DeclarativeBase):
    pass