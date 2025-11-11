from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from rusoft.config import DatabaseConfig


def new_session_maker(config: DatabaseConfig) -> async_sessionmaker[AsyncSession]:
    engine = create_async_engine(
        config.sqlalchemy_uri,
        pool_size=15,
        max_overflow=15,
        connect_args={
            "connect_timeout": 5,
        },
    )
    return async_sessionmaker(
        engine, class_=AsyncSession, autoflush=False, expire_on_commit=False
    )