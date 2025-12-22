from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# # Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (not recommended for production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
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


from pathlib import Path

app.mount(
    "/static",
    StaticFiles(
        directory=Path(__file__).parent / "static",
    ),
)


@app.middleware("http")
async def log_requests(request, call_next):
    print(f"Incoming request by method log_requests: {request.method} {request.url}")
    response = await call_next(request)
    print(f"Response status by method log_requests: {response.status_code}")
    return response


class LogRequestsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        print(
            f"Incoming request by class LogRequestsMiddleware: {request.method} {request.url}"
        )
        response = await call_next(request)
        print(
            f"Response status by class LogRequestsMiddleware: {response.status_code}",
        )
        return response


# add LogRequestsMiddleware
app.add_middleware(LogRequestsMiddleware)


# Endpoint that would typically require CORS
@app.get("/items/")
async def get_items():
    return [{"item": "Foo"}, {"item": "Bar"}]


@app.post("/items/")
async def create_item(item: dict):
    return {"message": "Item created", "item": item}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
    )
