from uuid import UUID, uuid4
from src.models.user import User, UserBase
from typing import Optional, Tuple
from src.infra.db import users
from sqlalchemy.dialects.postgresql import insert


def get(user_id: UUID) -> Optional[User]:
    result = users.select().where(
        users.c.id == user_id).execute().first()
    return User(**result) if result else None


def get_all() -> Optional[Tuple[User]]:
    results = users.select().execute().fetchall()
    return tuple(map(lambda x: User(**x), results)) if results else None


def delete(user_id: UUID) -> None:
    users.delete().where(
        users.c.id == user_id).execute()


def add(user: UserBase):
    user = User(id=uuid4(), **user.dict())
    insert(users).values(**user.dict()).execute()
    return user
