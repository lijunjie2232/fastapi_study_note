from typing import Annotated
from fastapi import (
    FastAPI,
    Query,
    Path,
    Form,
    Cookie,
    Header,
    Request,
    File,
    UploadFile,
    HTTPException,
)

from pydantic import BaseModel, Field, field_validator
import re

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
    size: int = Query(
        ...,
        gt=0,
        lt=10,
    ),
    name: str = Query(
        ...,
        min_length=1,
        max_length=10,
    ),
    email: str = Query(
        ...,
        pattern="^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+/.[a-zA-Z0-9-.]+$",
    ),
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


# form params
@app.post("/form_params")
async def form_params(
    name: str = Form(
        ...,
        description="name",
        min_length=1,
        max_length=10,
    ),
    age: int = Form(
        ...,
        description="age",
        gt=0,
        lt=10,
    ),
):
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


# raw(json)
class RegisterInfo(BaseModel):
    usename: str
    email: str
    password: str = Field(
        ...,
        min_length=8,
        max_length=50,
    )

    @field_validator("password")
    def password_must_meet_requirements(cls, v):
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one number")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("Password must contain at least one punctuation mark")
        return v


@app.post("/raw")
async def raw(register_info: RegisterInfo):
    """_summary_

    Args:
        register_info (RegisterInfo): register_info

    Returns:
        (dict)
    """
    return {
        "message": "Hello World",
        "code": 200,
        "data": {
            "register_info": register_info,
        },
    }


# cookie params
@app.get("/cookie_params")
async def cookie_params(
    token: Annotated[str | None, Cookie(...)] = None,
):
    """_summary_

    Args:
        token (str): token

    Returns:
        (dict)
    """
    return {
        "message": "Hello World",
        "code": 200,
        "data": {
            "token": token,
        },
    }


# header params
@app.get("/header_params")
async def header_params(
    bearer: Annotated[str | None, Header(...)] = None,
):
    """_summary_

    Args:
        bearer (str): token

    Returns:
        (dict)
    """
    return {
        "message": "Hello World",
        "code": 200,
        "data": {
            "token": bearer,
        },
    }


# request object
@app.get("/request_object/{path_id}")
async def request_object(request: Request, path_id: int = 0):
    """_summary_

    Args:
        request (Request): request

    Returns:
        (dict)
    """
    # print request info
    print(request.headers)
    print(request.cookies)
    print(request.query_params)
    print(request.path_params)
    return {
        "message": "Hello World",
        "code": 200,
        "data": {
            "token": request.headers.get("bearer"),
        },
    }


# upload file
@app.post("/file")
async def file(file: bytes = File(...)):
    """_summary_

    Args:
        file (bytes): file

    Returns:
        (dict)
    """

    return {
        "message": "Hello World",
        "code": 200,
        "data": {
            "file size": len(file),
        },
    }


@app.post("/upload_file")
async def upload_file(file: UploadFile):
    """_summary_
    Args:
        file (UploadFile): file

    Returns:
        (dict)
    """
    return {
        "message": "Hello World",
        "code": 200,
        "data": {
            "file name": file.filename,
            "file type": file.content_type,
        },
    }


# multiple files
@app.post("/multiple_files")
async def multiple_files(files: list[UploadFile]):
    """_summary_
    Args:
        files (list[UploadFile]): files

    Returns:
        (dict)
    """
    return {
        "message": "Hello World",
        "code": 200,
        "data": {
            "file name": [file.filename for file in files],
            "file type": [file.content_type for file in files],
        },
    }


# file upload and verify
import hashlib
from pathlib import Path

_ROOT_ = Path(__file__).parent.resolve()
_FILE_UPLOAD_DIR = _ROOT_ / "file_upload"
_FILE_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@app.post("/file_upload_and_verify")
async def file_upload_and_verify(
    file: UploadFile = File(...),
    md5: str = Form(""),
):
    """_summary_

    Args:
        file (UploadFile, optional): _description_. Defaults to File(...).
        md5 (str, optional): _description_. Defaults to Form(...).
    """
    if hashlib.md5(file.file.read()).hexdigest() != md5:
        # return {
        #     "message": "Hello World",
        #     "code": 400,
        #     "data": {
        #         "error": "md5 verify failed",
        #     },
        # }
        raise HTTPException(status_code=400, detail="md5 verify failed")
    else:
        file.file.seek(0)
        with open(_FILE_UPLOAD_DIR / str(file.filename), "wb") as f:
            f.write(file.file.read())

        return {
            "message": "Hello World",
            "code": 200,
            "data": {
                "file name": file.filename,
                "file type": file.content_type,
            },
        }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
