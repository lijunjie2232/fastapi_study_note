from fastapi import FastAPI, Query, Path

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
@app.get("/query_check")
async def query_check(
    size: int = Query(..., gt=0, lt=10),
    name: str = Query(..., min_length=1, max_length=10),
    email: str = Query(..., pattern="^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"),
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


# path params
@app.get("/path_params/{page_num}")
async def path_params(page_num: int, page_nums: int = 10):
    """_summary_

    Args:
        page_num (int): page_num
        page_nums (int): page_nums

    Returns:
        (dict)
    """
    return {
        "message": "Hello World",
        "code": 200,
        "data": {
            "page_num": page_num,
        },
    }


# path params check
@app.get("/path_params_check/{page_num}")
async def path_params_check(
    page_num: int = Path(..., gt=0, lt=10),
):
    """_summary_

    Args:
        page_num (int): page_num

    Returns:
        (dict)
    """
    return {
        "message": "Hello World",
        "code": 200,
        "data": {
            "page_num": page_num,
        },
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
