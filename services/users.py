from typing import Optional

from peewee import fn

from data.config import ADMINS
from models import User
from utils.misc.logging import logger


def count_users() -> int:
    query = User.select(fn.COUNT(User.id))
    return query.scalar()


def get_users() -> list[User]:
    query = User.select()

    return list(query)


def get_user(id: int) -> User:
    return User.get_or_none(User.id == id)


def update_user(user: User, name: str, username: str = None) -> User:
    user.name = name
    user.username = username
    user.save()

    return user


def edit_user_language(id: int, language: str):
    query = User.update(language=language).where(User.id == id)
    query.execute()


def create_user(id: int, name: str, username: str = None, language: str = None) -> User:
    new_user = User.create(id=id, name=name, username=username, language=language)

    if id in ADMINS:
        new_user.is_admin = True
        new_user.save()

    logger.info(f'New user {new_user}')

    return new_user


def get_or_create_user(id: int, name: str, username: str = None, language: str = None) -> User:
    user = get_user(id)

    if user:
        user = update_user(user, name, username)

        return user

    return create_user(id, name, username, language)


def get_admins() -> list[User]:
    query = User.filter(User.is_admin)
    return list(query)


def increase_balance(user_id: int, amount: int):
    query = User.get_or_none(User.id == user_id)
    query.balance += amount
    query.save()


def decrease_balance(user_id: int, amount: int):
    query = User.get_or_none(User.id == user_id)
    query.balance -= amount
    query.save()


def find_user(id_or_username: str) -> Optional[User]:
    try:
        int_id = int(id_or_username)
        query = User.get_or_none(User.id == int_id)
        if query:
            return query
    except:
        query = User.get_or_none(User.username == id_or_username)
        if query:
            return query

    return None


def make_admin(user: User) -> None:
    user.is_admin = True
    user.save()


def remove_admin(user: User) -> None:
    user.is_admin = False
    user.save()
