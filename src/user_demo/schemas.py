from datetime import datetime

from pydantic import BaseModel, Field


class RegisterForm(BaseModel):
    username: str = Field(
        ..., min_length=3, max_length=50, description="The user's username"
    )
    email: str = Field(
        ..., pattern=r"^\S+@\S+\.\S+$", description="The user's email address"
    )
    password: str = Field(..., min_length=8, description="The user's password")
    password_confirm: str = Field(
        ..., min_length=8, description="The user's password confirmation"
    )

    # validator for password
    @classmethod
    def validate_passwords(cls, values):
        if values.get("password") != values.get("password_confirm"):
            raise ValueError("Passwords do not match")
        return values

    # # validator for email
    # @classmethod
    # def validate_email(cls, values):
    #     email = values.get("email")
    #     return values


class LoginForm(BaseModel):
    email: str = Field(
        ..., pattern=r"^\S+@\S+\.\S+$", description="The user's email address"
    )
    password: str = Field(..., min_length=8, description="The user's password")


class UserInfo(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime
