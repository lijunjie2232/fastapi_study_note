from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

from sqlite_util import (
    create_user,
    authenticate_user,
    TORTOISE_ORM,
    get_user_by_id,
)
from jwt_util import create_access_token, decode_jwt
from tortoise.contrib.fastapi import register_tortoise

app = FastAPI()

register_tortoise(
    app,
    config=TORTOISE_ORM,
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.post("/users/register")
async def signup(username: str, email: str, password: str):
    user = await create_user(username, email, password)
    if not user:
        raise HTTPException(status_code=400, detail="email already registered")
    oauth2_token = create_access_token(
        data={
            "sub": user.id,
        },
    )
    return {"access_token": oauth2_token, "token_type": "bearer"}


@app.post("/users/login")
async def login(email: str, password: str):
    # Dummy login logic for demonstration
    user = await authenticate_user(email, password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    oauth2_token = create_access_token(
        data={
            "sub": user.id,
        },
    )
    return {"access_token": oauth2_token, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    payload = decode_jwt(token)
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return get_user_by_id(user_id)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
    )
