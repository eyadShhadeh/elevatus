from src.models.candidate import Gender
from sqlalchemy import Enum
import os
import uuid
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import (
    Boolean, Column, DateTime, Float, SmallInteger, Text, UniqueConstraint
)
from sqlalchemy.dialects.postgresql import ARRAY, UUID

pool_size = int(os.getenv('SQLALCHEMY_POOL_SIZE', 10))


def get_db_url():
    return 'postgresql://%s:%s@%s:%s/%s' % (
        os.getenv('PGUSER', 'postgres'),
        os.getenv('PGPASSWORD', 'password'),
        os.getenv('PGHOST', 'elevatus-service-db'),
        os.getenv('PGPORT', '5432'),
        os.getenv('PGDATABASE', 'postgres'),
    )


engine = sa.create_engine(get_db_url(), echo=False,
                          echo_pool=True, pool_size=pool_size, max_overflow=16)

metadata = sa.MetaData()
metadata.bind = engine

now = datetime.utcnow
default_now = dict(default=now, server_default=sa.func.now())

users = sa.Table(
    'users',
    metadata,
    Column('id', UUID(as_uuid=True), primary_key=True),
    Column('first_name', Text),
    Column('last_name', Text),
    Column('email', Text),
    Column('created_at', sa.DateTime(), server_default=sa.text('now()')),
    Column('updated_at', DateTime, onupdate=now, **default_now),
)

candidates = sa.Table(
    'candidates',
    metadata,
    Column('id', UUID(as_uuid=True), primary_key=True),
    Column('first_name', Text),
    Column('last_name', Text),
    Column('email', Text),
    Column('career_level', Text),
    Column('job_major', Text),
    Column('years_of_experience', SmallInteger),
    Column('skills', ARRAY(Text)),
    Column('nationality', Text),
    Column('city', Text),
    Column('salary', Float),
    Column('gender', Enum(Gender)),
    Column('created_at', sa.DateTime(), server_default=sa.text('now()')),
    Column('updated_at', DateTime, onupdate=now, **default_now),
)
