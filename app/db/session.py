from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings



async_engine = create_async_engine(settings.DATABASE_URL_asyncpg, echo = True)

async_session = async_sessionmaker(async_engine, expire_on_commit = False)


class Base(DeclarativeBase):
    pass

