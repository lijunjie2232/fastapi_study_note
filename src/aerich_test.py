from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

app = FastAPI()


TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.mysql",
            "credentials": {
                "host": "127.0.0.1",
                "port": "13306",
                "user": "root",
                "password": "password",
                "database": "aerich_test",
            },
        },
    },
    "apps": {
        "models": {
            "models": ["aerich.models", "src.orm_test"],
            "default_connection": "default",
        },
    },
}


if __name__ == "__main__":
    register_tortoise(
        app,
        config=TORTOISE_ORM,
    )
    import uvicorn

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="debug",
    )
