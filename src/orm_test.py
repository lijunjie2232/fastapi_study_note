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
    DatetimeField,
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
    # Age field as an integer, optional
    age = IntField(
        default=0,
        description="Age field as an integer, optional",
    )
    # amount field as an integer, optional
    amount = IntField(
        default=0,
        description="Amount field as an integer, optional",
    )
    # Password field with maximum length of 255 characters
    password = CharField(max_length=255)
    # Boolean field indicating if user is active, defaults to True
    is_active = BooleanField(default=True)
    # Boolean field indicating if user is superuser, defaults to False
    is_superuser = BooleanField(default=False)
    # create time
    created_at = DatetimeField(
        null=True,
        description="Creation timestamp",
        auto_now_add=True,
    )
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


async def do_create_user():
    # Example function to create a new user
    import random

    for i in range(100):
        user = await User.get_or_create(
            username=f"john_doe_{i}",
            email=f"john_doe_{i}@example.com",
            password="password",
            age=random.randint(18, 60),
            amount=random.randint(100, 1000),
            is_active=random.choice([True, False]),
            is_superuser=random.choice([True, False]),
        )
        print(f"Created user: {user}")


async def do_query_users():
    # Example function to query all users
    users = await User.all()
    for user in users:
        print(f"User: {user}, Email: {user.email}")


async def do_update_user():
    # Example function to update a user
    user = await User.get(username="john_doe_1")
    user.email = "john@example.com"
    await user.save()
    print(f"Updated user: {user}")


async def do_delete_user():
    # Example function to delete a user
    user = await User.get(username="john_doe_1")
    await user.delete()
    print(f"Deleted user: {user}")


async def advanced_query():
    # get method
    # user = await User.get(password="password")
    # print(user)
    user = await User.get(username="john_doe_2")
    print(user)
    user = await User.get_or_none(username="non_existent_user")
    print(user)

    # Basic filtering
    users = await User.filter(is_active=True)
    print(f"Active users: {users}")

    # Complex conditions with operators
    users = await User.filter(username__icontains="john")
    print(f"Users with 'john' in username: {users}")

    # Multiple conditions (AND by default)
    users = await User.filter(is_active=True, is_superuser=False)
    print(f"Active non-superuser users: {users}")

    # update Active status for users
    await User.filter(is_active=True).update(is_superuser=False)

    # OR conditions using Q objects
    from tortoise.expressions import Q

    users = await User.filter(Q(username="john") | Q(email="john@example.com"))
    print(f"Users with username 'john' or email 'john@example.com': {users}")

    # Order results
    users = await User.all().order_by("-created_at")
    print(f"Users ordered by creation date descending: {users}")

    # Limit results (pagination)
    users = await User.all().limit(10).offset(20)
    print(f"Users with limit and offset: {users}")

    # Count records
    count = await User.filter(is_active=True).count()
    print(f"Count of active users: {count}")

    # Get minimum/maximum values
    min_age = await User.all().min("age")
    max_age = await User.all().max("age")
    print(f"Minimum age: {min_age}, Maximum age: {max_age}")

    # Sum and average calculations
    total_orders = await Order.all().sum("total_amount")
    avg_order = await Order.all().avg("total_amount")
    print(f"Total order amount: {total_orders}, Average order amount: {avg_order}")
    return

    # Access related objects directly
    user = await User.get(id=1)
    orders = await user.orders.all()  # Get all orders for a user

    # Filter on related objects
    paid_orders = await Order.filter(user__is_active=True, is_paid=True)

    # Access reverse relations
    user = await User.get(id=1)
    user_orders = await user.orders.all()  # Using the ReverseRelation

    # Optimize queries by prefetching related data
    users = await User.all().prefetch_related("orders", "userinfo")
    for user in users:
        # No additional DB queries needed for these relations
        print(user.orders)
        print(user.userinfo)

    # Add computed fields to queryset
    from tortoise.functions import Count

    users_with_order_count = await User.annotate(order_count=Count("orders")).filter(
        order_count__gt=0
    )

    # Execute raw SQL when needed
    users = await User.raw("SELECT * FROM users WHERE is_active = %s", [True])

    # Perform atomic operations
    from tortoise.transactions import in_transaction

    async with in_transaction() as connection:
        user = await User.create(username="test", email="test@example.com")
        await UserInfo.create(user=user, full_name="Test User")
        # Both operations commit together or rollback together


if __name__ == "__main__":
    # Run the async initialization function
    run_async(init())
    print("================Database initialized and schemas generated.================")

    # Run the async functions
    # print("================Creating new users...================")
    # run_async(do_create_user())
    # print("================Querying all users...================")
    # run_async(do_query_users())
    # print("================Updating a user...================")
    # run_async(do_update_user())
    # print("================Querying all users after update...================")
    # run_async(do_query_users())
    # print("================Deleting a user...================")
    # run_async(do_delete_user())
    # print("================Querying all users after deletion...================")
    # run_async(do_query_users())
    print("================Advanced query examples...================")
    run_async(advanced_query())
