from fastapi import FastAPI, Query

app = FastAPI()


# query params
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


# query check
app.get("/query_check")


async def query_check(
    size: int = Query(..., gt=0, lt=10),
    name: str = Query(..., min_length=1, max_length=10),
    email: str = Query(..., regex="^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"),
):
    """_summary_

    Args:
        size (int): size
        name (str): name
        email (str): email

    Returns:
        (dict)
    """
    return {
        "message": "Hello World",
        "code": 200,
        "data": {
            "size": size,
            "name": name,
            "email": email,
        },
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
