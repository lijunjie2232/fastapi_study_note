from fastapi import FastAPI

app = FastAPI(
    title="FastAPI Study Note",
    description="FastAPI Study Note",
    version="0.1.0",
    openapi_url="/api/openapi.json",
    exception_handlers={},
)


@app.get("/")
async def root() -> dict:
    return {
        "message": "Hello World",
        "code": 200,
        "data": {
            "name": "FastAPI Study Note",
            "version": "0.1.0",
        },
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
    )
