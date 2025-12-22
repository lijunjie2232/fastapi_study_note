from fastapi import FastAPI
from exceptions import (
    http_exception_handler,
    InsufficientFundsError,
    insufficient_handler,
)
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI(
    title="FastAPI Study Note",
    description="FastAPI Study Note",
    version="0.1.0",
    openapi_url="/api/openapi.json",
)

app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(InsufficientFundsError, insufficient_handler)


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


@app.get("/exception_test")
async def exception_test() -> dict:
    raise StarletteHTTPException(
        status_code=400, detail="This is a custom exception test."
    )


@app.post("/buy-coffee")
def buy_coffee(balance: float = 10.0) -> dict:
    price = 15.0
    if balance < price:
        raise InsufficientFundsError(balance, price)
    return {"msg": "☕ 已下单！老板说送你一块曲奇～"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
    )
