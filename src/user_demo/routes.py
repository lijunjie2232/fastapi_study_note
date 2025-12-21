from fastapi import HTTPException, APIRouter

from models import UserModel
from schemas import LoginForm, RegisterForm, UserInfo

user_router_v1 = APIRouter(prefix="/api/v1/user")


@user_router_v1.post("/register", response_model=UserInfo)
async def register_user(item: RegisterForm):
    """Register a new user."""
    user = await UserModel.create(**item.model_dump(exclude={"password_confirm"}))
    return UserInfo.model_validate(user.__dict__)


@user_router_v1.post("/login", response_model=UserInfo)
async def login_user(item: LoginForm):
    """Login an existing user."""
    user = await UserModel.get_or_none(email=item.email, password=item.password)
    if not user:
        return HTTPException(status_code=400, detail="Invalid credentials")
    return UserInfo.model_validate(user.__dict__)
