import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import clear_mappers, sessionmaker

from app.database.schema import load_mappers, mapper_registry


@pytest.fixture
def in_memory_db():
    engine = create_engine("sqlite:///:memory:")
    mapper_registry.metadata.create_all(engine)
    return engine


@pytest.fixture
def session(in_memory_db):
    load_mappers()
    yield sessionmaker(bind=in_memory_db)()
    clear_mappers()
