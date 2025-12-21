import uvicorn
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from routes import user_router_v1

app = FastAPI()

app.include_router(user_router_v1)


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


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
