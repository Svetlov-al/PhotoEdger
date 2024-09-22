import pytest
import redis
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tenacity import retry, stop_after_delay

from src.image import config
from src.image.adapters.orm import metadata, start_mappers
from src.image.core.main import app

pytest.register_assert_rewrite("tests.e2e.api_client")


@pytest.fixture
def in_memory_sqlite_db():
    engine = create_engine("sqlite:///:memory:")
    metadata.create_all(engine)
    return engine


@pytest.fixture
def sqlite_session_factory(in_memory_sqlite_db):
    yield sessionmaker(bind=in_memory_sqlite_db)


@pytest.fixture
def mappers():
    start_mappers()


@retry(stop=stop_after_delay(10))
def wait_for_postgres_to_come_up(engine):
    return engine.connect()


@retry(stop=stop_after_delay(10))
def wait_for_redis_to_come_up():
    r = redis.Redis(**config.get_redis_host_and_port())
    return r.ping()


@pytest.fixture(scope="session")
def postgres_engine():
    engine = create_engine(config.get_postgres_uri())
    yield engine
    engine.dispose()


@pytest.fixture(scope="session", autouse=True)
def setup_postgres(postgres_engine):
    """Создание таблиц для тестовой базы в начале сессии"""
    wait_for_postgres_to_come_up(postgres_engine)

    metadata.create_all(postgres_engine)

    yield

    metadata.drop_all(postgres_engine)


@pytest.fixture
def postgres_session_factory(postgres_engine, setup_postgres):
    yield sessionmaker(bind=postgres_engine, expire_on_commit=False)


@pytest.fixture
def postgres_session(postgres_session_factory):
    return postgres_session_factory()


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client
