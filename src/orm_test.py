from typing import Optional

from tortoise import (
    Tortoise,
    run_async,
    Model,
)
from tortoise.fields import (
    IntField,
    CharField,
    BooleanField,
)


# Define User model that inherits from Tortoise's Model class
class User(Model):
    # Primary key field with auto increment
    id = IntField(
        pk=True,
        auto_increment=True,
    )
    # Username field with maximum length of 255 characters and unique constraint
    username = CharField(
        max_length=255,
        unique=True,
    )
    # Email field with maximum length of 255 characters and unique constraint
    email = CharField(
        max_length=255,
        unique=True,
    )
    # Password field with maximum length of 255 characters
    password = CharField(max_length=255)
    # Boolean field indicating if user is active, defaults to True
    is_active = BooleanField(default=True)
    # Boolean field indicating if user is superuser, defaults to False
    is_superuser = BooleanField(default=False)

    def __str__(self) -> str:
        return self.username


async def init():
    # Initialize Tortoise ORM with MySQL database connection
    await Tortoise.init(
        db_url="mysql://root:password@127.0.0.1:13306/fastapi_dev",
        # Register models module - using __main__ for this example
        modules={"models": ["__main__"]},
    )

    # Generate database schemas based on defined models
    await Tortoise.generate_schemas(safe=True)


if __name__ == "__main__":
    # Run the async initialization function
    run_async(init())
    print("Database initialized and schemas generated.")
