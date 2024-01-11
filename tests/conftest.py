from fastapi.testclient import TestClient
from src.main import app
from pytest import fixture
from src.infra.db import engine, get_db_url
from sqlalchemy import text
from alembic.command import upgrade
from alembic.config import Config


@fixture
def client():
    return TestClient(app)


@fixture(scope='session')
def db() -> None:
    config = Config('alembic.ini')
    config.set_main_option(
        'sqlalchemy.url',
        get_db_url()
    )
    engine.execute('DROP SCHEMA IF EXISTS public CASCADE')
    engine.execute('CREATE SCHEMA public')
    upgrade(config, 'head')


@fixture(autouse=True)
def clear_tables() -> None:
    with engine.connect() as conn:
        conn.execute(text('TRUNCATE TABLE users CASCADE'))
        conn.execute(text('TRUNCATE TABLE candidates CASCADE'))
