import uvicorn
from fastapi import FastAPI, HTTPException
from tortoise.contrib.fastapi import register_tortoise

from models import UserModel
from schemas import LoginForm, RegisterForm, UserInfo

app = FastAPI()

# configure tortoise-orm here (omitted for brevity)
TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.mysql",
            "credentials": {
                "host": "127.0.0.1",
                "port": "13306",
                "user": "root",
                "password": "password",
                "database": "fastapi_db_test",
            },
        },
    },
    "apps": {
        "models": {
            "models": ["aerich.models", "models"],
            "default_connection": "default",
        },
    },
}

register_tortoise(app, config=TORTOISE_ORM)


@app.post("/api/v1/users/register", response_model=UserInfo)
async def register_user(item: RegisterForm):
    """Register a new user."""
    user = await UserModel.create(**item.model_dump(exclude={"password_confirm"}))
    return UserInfo.model_validate(user.__dict__)


@app.post("/api/v1/users/login", response_model=UserInfo)
async def login_user(item: LoginForm):
    """Login an existing user."""
    user = await UserModel.get_or_none(email=item.email, password=item.password)
    if not user:
        return HTTPException(status_code=400, detail="Invalid credentials")
    return UserInfo.model_validate(user.__dict__)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
