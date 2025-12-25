# sqlite client and schema

from tortoise import Tortoise, Model
from tortoise.fields import CharField, IntField, BooleanField

from pass_util import get_password_hash, verify_password

TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.sqlite",
            "credentials": {"file_path": "db.sqlite3"},
        },
    },
    "apps": {
        "models": {
            "models": ["aerich.models", "sqlite_util"],
            "default_connection": "default",
        },
    },
}


################### User Schema ###################


class User(Model):
    id = IntField(
        pk=True,
        auto_increment=True,
        description="id of user",
    )
    username = CharField(
        max_length=255,
        description="username of user",
    )
    email = CharField(
        max_length=255,
        description="email of user",
    )
    password_hash = CharField(
        max_length=255,
        description="hashed password of user",
    )
    is_active = BooleanField(
        default=True,
        description="is user active",
    )


################### User Service ###################


async def create_user(username, email, password):
    if await User.get_or_none(email=email):
        return None
    user = await User.create(
        username=username,
        email=email,
        password_hash=await get_password_hash(password),
    )
    return user


async def authenticate_user(email: str, password: str):
    user = await User.get_or_none(email=email)
    if not user:
        return None
    if not await verify_password(password, user.password_hash):
        return None
    return user


async def get_user_by_id(id: int):
    user = await User.get_or_none(id=id)
    return user
