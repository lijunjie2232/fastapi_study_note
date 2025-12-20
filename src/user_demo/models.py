from tortoise import fields, models


class UserModel(models.Model):
    """_summary_
    User model representing a user in the system.
    Attributes:
        id (int): Primary key.
        username (str): Unique username of the user.
        email (str): Unique email address of the user.
        sex (str): Sex of the user.
        age (int): Age of the user.
        is_active (bool): Status indicating if the user is active.
        created_at (datetime): Timestamp of user creation.
    """

    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    email = fields.CharField(max_length=100, unique=True)
    sex = fields.CharField(max_length=10, null=True)
    age = fields.IntField(null=True)
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    password = fields.CharField(max_length=100)

    def __str__(self):
        return self.username

    class Meta:
        table = "users"
        table_description = "User model"
