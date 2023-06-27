from sqlalchemy.orm import clear_mappers
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
)
import pytest_asyncio

from schema import mapper_registry, load_mappers


@pytest_asyncio.fixture
async def in_memory_db():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as connection:
        await connection.run_sync(mapper_registry.metadata.create_all)
    return engine


@pytest_asyncio.fixture
async def session(in_memory_db):
    load_mappers()
    yield async_sessionmaker(in_memory_db, expire_on_commit=False)
    clear_mappers()
