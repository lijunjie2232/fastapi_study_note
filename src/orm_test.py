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
    ForeignKeyField,
    ReverseRelation,
    OneToOneField,
    ManyToManyField,
)


# Define User model that inherits from Tortoise's Model class
class User(Model):
    # Primary key field with auto increment
    id = IntField(
        pk=True,
        auto_increment=True,
        description="Primary key field with auto increment",
    )
    # Username field with maximum length of 255 characters and unique constraint
    username = CharField(
        max_length=255,
        unique=True,
        description="Username field with maximum length of 255 characters and unique constraint",
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
    # reverse relation to Other models
    orders: ReverseRelation["Order"]
    userinfo: ReverseRelation["UserInfo"]
    groups: ReverseRelation["Group"]

    def __str__(self) -> str:
        return self.username

    class Meta:
        table = "users"  # Specify custom table name
        table_description = "User table"  # Description for the table


# One-to-One relationship example
class UserInfo(Model):
    id = IntField(
        pk=True,
        auto_increment=True,
        description="Primary key field with auto increment",
    )
    user = OneToOneField(
        "models.User",
        related_name="userinfo",
        description="Foreign key field to link to User model",
    )
    full_name = CharField(
        max_length=255,
        description="Full name of the user",
    )
    address = CharField(
        max_length=500,
        description="Address of the user",
    )
    phone_number = CharField(
        max_length=20,
        description="Phone number of the user",
    )

    def __str__(self) -> str:
        return self.full_name

    class Meta:
        table = "user_info"  # Specify custom table name
        table_description = "User Info table"  # Description for the table


# Many-to-One relationship example
class Order(Model):
    id = IntField(
        pk=True,
        auto_increment=True,
        description="Primary key field with auto increment",
    )
    order_number = CharField(
        max_length=100,
        unique=True,
        description="Order number with maximum length of 100 characters and unique constraint",
    )
    user = ForeignKeyField(
        "models.User",
        related_name="orders",
        description="Foreign key field to link to User model",
    )
    total_amount = IntField(
        description="Total amount for the order",
    )
    is_paid = BooleanField(default=False)

    def __str__(self) -> str:
        return self.order_number

    class Meta:
        table = "orders"  # Specify custom table name
        table_description = "Order table"  # Description for the table


# Many-to-Many relationship example
class Group(Model):
    id = IntField(
        pk=True,
        auto_increment=True,
        description="Primary key field with auto increment",
    )
    name = CharField(
        max_length=100,
        unique=True,
        description="Group name with maximum length of 100 characters and unique constraint",
    )
    members = ManyToManyField(
        "models.User",
        related_name="groups",
        description="Many-to-Many relationship to User model",
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        table = "groups"  # Specify custom table name
        table_description = "Group table"  # Description for the table


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
