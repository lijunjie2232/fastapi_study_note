from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import JSONResponse
from fastapi.requests import Request


# @app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    # custom handling for global parameters error
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": exc.detail,
            "code": exc.status_code,
            "data": None,
        },
    )


class InsufficientFundsError(Exception):
    def __init__(self, balance: float, needed: float):
        self.balance = balance
        self.needed = needed
        super().__init__(f"余额 {balance} < 需要 {needed}")


# 注册处理器（用 add_exception_handler 更显高级 😎）
def insufficient_handler(request: Request, exc: InsufficientFundsError):
    return JSONResponse(
        status_code=402,  # 402 Payment Required 是正经 HTTP 状态码！
        content={
            "code": "BALANCE_TOO_LOW",
            "message": "钱包比脸还干净 😭",
            "current": exc.balance,
            "required": exc.needed,
            "tip": "要不要… 充个 10 块？",
        },
    )
