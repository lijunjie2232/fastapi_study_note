from fastapi import APIRouter, Depends, Header, HTTPException
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


async def fake_oauth2(_):
    return "123@abcd.com"


async def token_validate(token=Header(...)):
    """Validate a token."""
    if token != "123321":
        raise HTTPException(status_code=400, detail="Invalid token")


@user_router_v1.get(
    "/me",
    response_model=UserInfo,
)
async def me(token: str = Depends(token_validate)):
    """Get the current user."""
    print(await fake_oauth2(token))
    user = await UserModel.get_or_none(email=await fake_oauth2(token))
    if not user:
        raise HTTPException(status_code=400, detail="Invalid token")
    return UserInfo.model_validate(user.__dict__)
