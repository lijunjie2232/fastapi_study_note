from fastapi import FastAPI

app = FastAPI()


@app.get("/query_params")
async def query_params(name: str, age: int | None = 0):
    """_summary_

    Args:
        name (str): name
        age (int): age

    Returns:
        (dict)
    """
    return {
        "message": "Hello World",
        "code": 200,
        "data": {
            "name": name,
            "age": age,
        },
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
