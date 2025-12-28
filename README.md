# fastapi_study_note

このノートでは、FastAPIを使って、APIを書く方法を学んでいきます。

- [fastapi\_study\_note](#fastapi_study_note)
  - [Installation](#installation)
  - [pydantic](#pydantic)
    - [JSON Schema](#json-schema)
    - [pydantic型転換](#pydantic型転換)
    - [pydantic Field](#pydantic-field)
  - [スタート](#スタート)
  - [fastapi request and response](#fastapi-request-and-response)
    - [query parameters](#query-parameters)
      - [example](#example)
      - [デフォルト値の設定：](#デフォルト値の設定)
      - [query check](#query-check)
        - [example](#example-1)
        - [`Query`](#query)
    - [path parameters](#path-parameters)
      - [example](#example-2)
      - [path parameters check](#path-parameters-check)
        - [example](#example-3)
      - [`Path`](#path)
    - [request body](#request-body)
      - [Form](#form)
      - [RAW JSON](#raw-json)
    - [request cookies](#request-cookies)
    - [request headers](#request-headers)
    - [request object](#request-object)
    - [request upload file](#request-upload-file)
      - [Method 1 (byte file)](#method-1-byte-file)
      - [Method 2 (UploadFile object) (recommended)](#method-2-uploadfile-object-recommended)
    - [file upload and verify](#file-upload-and-verify)
    - [response status code](#response-status-code)
    - [response model](#response-model)
    - [set cookie](#set-cookie)
    - [response header](#response-header)
  - [Tortoise ORM](#tortoise-orm)
    - [connection configuration](#connection-configuration)
    - [model definition](#model-definition)
      - [model fields](#model-fields)
    - [model relationship](#model-relationship)
      - [ForeignKeyField](#foreignkeyfield)
      - [OneToOneField](#onetoonefield)
      - [ManyToManyField](#manytomanyfield)
      - [Full Example](#full-example)
    - [sql operations](#sql-operations)
      - [Create user](#create-user)
      - [query users](#query-users)
      - [Update user](#update-user)
      - [delete user](#delete-user)
    - [Advanced Usage](#advanced-usage)
      - [filter](#filter)
        - [ambiguous conditions](#ambiguous-conditions)
        - [LIKE conditions](#like-conditions)
        - [and conditions](#and-conditions)
        - [`update`](#update)
        - [or conditions](#or-conditions)
        - [`order_by`](#order_by)
        - [`limit` and `offset`](#limit-and-offset)
        - [`count`](#count)
        - [access related objects](#access-related-objects)
      - [prefetch related objects](#prefetch-related-objects)
      - [`tortoise.functions`](#tortoisefunctions)
        - [Text Transformation Functions](#text-transformation-functions)
        - [Null Handling Functions](#null-handling-functions)
        - [Database-Specific Random Functions](#database-specific-random-functions)
        - [Aggregate Functions](#aggregate-functions)
        - [Example Usage](#example-usage)
        - [Usage Patterns](#usage-patterns)
      - [Execute raw SQL](#execute-raw-sql)
      - [Transactions](#transactions)
        - [`in_transaction`](#in_transaction)
        - [`atomic`](#atomic)
      - [execute raw SQL](#execute-raw-sql-1)
  - [Aerich](#aerich)
    - [Installation](#installation-1)
    - [Migration](#migration)
    - [Update Schema](#update-schema)
  - [**APIRouter**](#apirouter)
      - [Usage](#usage)
      - [Example](#example-4)
  - [Project Structure](#project-structure)
    - [Layered Architecture (Most Common)](#layered-architecture-most-common)
      - [Core Configuration (core/)](#core-configuration-core)
      - [Models and Schemas (models/, schemas/)](#models-and-schemas-models-schemas)
      - [API Organization](#api-organization)
      - [Data Access Layer](#data-access-layer)
    - [Feature-Based Structure (Advanced)](#feature-based-structure-advanced)
    - [Domain-Driven Design (DDD) Approach](#domain-driven-design-ddd-approach)
  - [**Dependency Injection**](#dependency-injection)
    - [Function Dependency Injection](#function-dependency-injection)
      - [authorization validation](#authorization-validation)
      - [database connection and initialization](#database-connection-and-initialization)
      - [log wreiting](#log-wreiting)
      - [Cache](#cache)
    - [Class Dependency Injection](#class-dependency-injection)
    - [Sub-Dependency Injection](#sub-dependency-injection)
    - [Dependency Injection in Path](#dependency-injection-in-path)
    - [Global Dependency Injection](#global-dependency-injection)
  - [FastAPI Configuration](#fastapi-configuration)
  - [Global Exception Handler](#global-exception-handler)
    - [exception\_handler decorator](#exception_handler-decorator)
    - [add\_exception\_handler method](#add_exception_handler-method)
    - [custom exception](#custom-exception)
  - [FastAPI Middleware](#fastapi-middleware)
    - [Configuration in FastAPI](#configuration-in-fastapi)
    - [Security Considerations](#security-considerations)
    - [**Custom Middleware**](#custom-middleware)
      - [CustomCORSMiddleware Class](#customcorsmiddleware-class)
      - [internal advanced middleware in FastAPI](#internal-advanced-middleware-in-fastapi)
    - [**Custom BaseHTTPMiddleware**](#custom-basehttpmiddleware)
  - [**Background Tasks**](#background-tasks)
    - [Demo Config](#demo-config)
    - [Email service](#email-service)
    - [Redis Client](#redis-client)
    - [Message Queue](#message-queue)
    - [FastAPI Server](#fastapi-server)
    - [Email Consumer](#email-consumer)
    - [docker compose file](#docker-compose-file)
    - [Run Demo](#run-demo)
  - [WebSockets Demo](#websockets-demo)
  - [OAuth2.0](#oauth20)
    - [passlib](#passlib)
      - [Usage](#usage-1)
    - [JWT (JSON Web Token)](#jwt-json-web-token)
      - [Usage](#usage-2)
    - [OAuth2.0 in FastAPI](#oauth20-in-fastapi)
      - [OAuth2PasswordBearer](#oauth2passwordbearer)
      - [Theory of OAuth2.0](#theory-of-oauth20)
      - [OAuth2.0 Demo](#oauth20-demo)
        - [main](#main)
        - [sqlite util](#sqlite-util)
        - [jwt util](#jwt-util)
  - [Asyncio](#asyncio)
    - [主要概念](#主要概念)
    - [Basic Usage](#basic-usage)
    - [event\_Loop](#event_loop)
    - [Task](#task)
  - [Future](#future)



## Installation

`pip install fastapi` でインストールします。
`pip install "uvicorn[standard]"` で、Uvicorn server もインストールします。

## pydantic

example code: [pydantic_test.py](src/pydantic_test.py)

pydanticは、Pythonの型チェックを行うライブラリです。

```python
from pydantic import BaseModel


class TestModel(BaseModel):
    id: int
    name: str
    age: int = 0 # デフォルト値


test_model2 = TestModel(
    id="2",
    name="Bob",
    age="25",
)
print_test_model(test_model2)
# id=2 name='Bob' age=25
```

- <font color="red">この例、idとageは整数型として定義されていますが、インスタンス作成時には文字列（id="2"、age="25"）で渡している点です。Pydanticは自動的に適切な型に変換してくれます。</font>

### JSON Schema

```python
print(test_model2.model_json_schema())
"""{'properties': {'age': {'title': 'Age', 'type': 'integer'},
                'id': {'title': 'Id', 'type': 'integer'},
                'name': {'title': 'Name', 'type': 'string'}},
 'required': ['id', 'name', 'age'],
 'title': 'TestModel',
 'type': 'object'}"""
```

### pydantic型転換

dict()メソッドを使用していますが、これはPydantic V2.0から**非推奨**となりました。同様に、json()メソッドも非推奨となっています。

新しいメソッドに置き換えることを推奨します：

- `dict()` → `model_dump()`
- `json()` → `model_dump_json()`
- `parse_obj()` → `model_validate()`
- `parse_raw()` → `model_validate_json()`

```python
print(test_model2.model_dump())
# {'id': 2, 'name': 'Bob', 'age': 25}
print(test_model2.model_dump_json())
# {"id":2,"name":"Bob","age":25}
```

```python
print(
    TestModel.model_validate(
        {
            "id": "2",
            "name": "Bob",
            "age": "25",
        }
    )
)
# TestModel(id=2, name='Bob', age=25)
print(TestModel.model_validate_json('{"id": "2", "name": "Bob", "age": "25"}'))
# TestModel(id=2, name='Bob', age=25)
```

```python
test_model3 = TestModel(
    id=3,
    name="Charlie",
) # age=0 がデフォルト値のまま
print_test_model(test_model3)
# id=3 name='Charlie' age=0
print(test_model3.model_dump())
# {'id': 3, 'name': 'Charlie', 'age': 0}
print(test_model3.model_dump(exclude_defaults=True))
# {'id': 3, 'name': 'Charlie'}
print(test_model3.model_dump(exclude_unset=True))
# {'id': 3, 'name': 'Charlie'}
print(test_model3.model_dump(exclude={"age"}))
# {'id': 3, 'name': 'Charlie'}
print(test_model3.model_dump(include={"id", "age"}))
# {'age': 0, 'id': 3}
```

### pydantic Field

pydanticのFieldクラスを使って、Pydanticモデルのフィールドを設定することができます。

```python
from pydantic import BaseModel, Field, field_validator
import re


class RegisterInfo(BaseModel):
    usename: str
    email: str
    password: str = Field(
        ...,
        min_length=8,
        max_length=50,
        pattern=r"^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?\":{}|<>]).*$",
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

```


## スタート

example code: [fastapi_start.py](src/fastapi_start.py)

```python
from fastapi import FastAPI

app = FastAPI() # ここでアプリケーションを初期化します。


@app.get("/") # ルートパスにアクセスしたときに実行される関数を定義します。
def root():
    return {"message": "Hello World"} # ここで返す値を指定します。

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    # ここでサーバーを起動します。
    # 0.0.0.0 はすべてのインターフェースを指します。
    # 8000 はポート番号です。
    # これで、http://localhost:8000/ にアクセスすると、Hello World が表示されます。

```


## fastapi request and response

example code: [requests_param.py](src/requests_param.py)

### query parameters

#### example
```python
@app.get("/query_params")
async def query_params(name: str, age: int | None = 0): 
    # ここでnameとageを取得します。
    # ageはデフォルト値として0を設定しています。
    return {
        "message": "Hello World",
        "code": 200,
        "data": {
            "name": name,
            "age": age,
        },
    }
```

#### デフォルト値の設定：
- `def query_params(age: int | None = 0)`
- `def query_size(size: Union[int, None] = 10)`

#### query check

use `Query` class to check query parameters.

##### example
```python
async def query_check(
    size: int = Query(..., gt=0, lt=10),
    name: str = Query(..., min_length=1, max_length=10),
    email: str = Query(..., regex="^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"),
):
    return {}
```

##### `Query`
```python
from fastapi import Query

query = Query(
    default, # デフォルト値
    alias=None, # 別名
    title=None, # タイトル
    description=None, # 説明
    required=True, # 必須かどうか
    deprecated=None, # 廃止かどうか
    ge=None, # [Number] 最小値 (inclusive)
    gt=None, # [Number] 最小値（ exclusive ）
    le=None, # [Number] 最大値 (inclusive)
    lt=None, # [Number] 最大値 (exclusive)
    multiple_of=None, # 倍数
    min_length=None, # [str] 最小文字数
    max_length=None, # [str] 最大文字数
    pattern=None, # [str] 正規表現 (regexは廃止)
    encoding=None, # [str] エンコーディング
    *args,
    **kwargs,
)
```

- もし、デフォルト値を設定しないばあしは、必ず先ずは`...`で指定します：`Query(..., gt=0, lt=10)`

### path parameters
#### example
```python
@app.get("/path_params/{page_num}")
# ここで、page_numを取得します。
async def path_params(
    page_num: int, # ここで、page_numはpathから渡す
    page_nums: int　# ここで、page_numsはクエリーから渡す（パスのパラメターには同じ名前のはない）
)
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
```

#### path parameters check
##### example
```python
@app.get("/path_params_check/{page_num}")
async def path_params_check(
    page_num: int = Path(..., gt=0, lt=10),
):
    pass
```

#### `Path`
`Path` は `Query` と同様に使用します。

### request body

request body は、`POST`、`PUT`、`PATCH` メソッドで使用します。

<font color="red">**注意</font>： "Request with GET/HEAD method cannot have body. "**

1. **Form Data**
   - ファイルアップロード時に使用
   - 例：ユーザー登録フォームでプロフィール画像をアップロードする場合
   ```
   POST /upload
   Content-Type: multipart/form-data
   
   name: "田中太郎"
   email: "tanaka@example.com"
   profile_image: [バイナリデータ]
   ```

   - multipart/form-data 形式では、ファイルを送信する際に特別な区切り文字（boundary / バウンダリ）が使用されます。
    ```
    POST /upload HTTP/1.1
    Content-Type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW

    ------WebKitFormBoundary7MA4YWxkTrZu0gW
    Content-Disposition: form-data; name="username"

    tanakatarou
    ------WebKitFormBoundary7MA4YWxkTrZu0gW
    Content-Disposition: form-data; name="profile"; filename="profile.jpg"
    Content-Type: image/jpeg

    [バイナリデータ]
    ------WebKitFormBoundary7MA4YWxkTrZu0gW--
    ```
    

2. **RAW**
   - API間通信でよく使われる（特にJSON形式）
   - 例：ユーザー情報をJSON形式で送信する場合
   ```
   POST /api/users
   Content-Type: application/json
   
   {
     "name": "山田花子",
     "age": 28,
     "email": "yamada@example.com"
   }
   ```

3. **x-www-form-urlencoded**
   - 従来のHTMLフォーム送信で使用
   - 形式は: `key=value`
   - 例：ログイン情報などを送信する場合
   ```
   POST /login
   Content-Type: application/x-www-form-urlencoded
   
   username=yamada&password=mypassword123
   ```

#### Form

```python
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
    pass
```

- `Form` は `Query` と同様に使用しますが：
    ```python
    # Query
    @app.get("/query_params")
    async def query_params(name: str, age: int | None = 0): pass

    # Form
    @app.post("/form_params")
    async def form_params(name: str = Form(...), age: int = Form(...)): pass
    ```

#### RAW JSON

JSON Data を受けるために、pydantic Model を使うべき

```python
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
```

### request cookies

request cookies は、`GET`、`POST`、`PUT`、`PATCH`、`DELETE` メソッドで使用します。
クッキーは、ブラウザーからサーバーに送信されるデータです。

```python
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
```

### request headers

- headers は、ブラウザーからサーバーに送信されるデータです。

- first use `from fastapi import Header` to import `Header`

```python
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
```

### request object

```python
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
```

### request upload file

- first install `python-multipart` by `pip install python-multipart`

#### Method 1 (byte file)

- this method receive file as bytes list, all content in file will be stored in memory

```python
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
```

#### Method 2 (UploadFile object) (recommended)

- this method receive file as file object, part of file will automaticly be stored in disk
- more meta info of file could be get from file object

```python
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

```

- properties of UploadFile class
    - `file`: Annotated[BinaryIO, Doc("The standard Python file object (non-async)."),]
    - `filename`: Annotated[Optional[str], Doc("The original file name.")]
    - `size`: Annotated[Optional[int], Doc("The size of the file in bytes.")]
    - `headers`: Annotated[Headers, Doc("The headers of the request.")]
    - `content_type`: Annotated[Optional[str], Doc("The content type of the request, from the headers.")]

- use `UploadFile.file.seek(0)` to reset file pointer

### file upload and verify

```python

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

```

### response status code

```python
@app.put("/add", status_code=fastapi.status.HTTP_201_CREATED)
...
```
- status code could be set in `@app.put()` or `return`

### response model

```python
# response model
class Result(BaseModel):
    message: str
    code: int = 200
    data: dict | None = None


@app.get("/items2", response_model=Result)
...

@app.get("/items3", response_model=List[Items])
...
```

### set cookie

- method 1: use response object in fastapi.responses, a response object should be constructed first, then set cookie by `response.set_cookie(k, v)`

```python
@app.get("/cookie", response_model=Result)
async def cookie(a: int, b: int):
    """_summary_

    Args:
        a (int): a
        b (int): b

    Returns:
        (JSONResponse)
    """
    response = JSONResponse(
        content=Result(
            message="Hello World",
            code=200,
            data={
                "result": a + b,
            },
        ).model_dump(),
        status_code=status.HTTP_200_OK,
    )
    response.set_cookie(
        key="_session_id",
        value="fake-session-id",
    )
    return response
```

- method 2: get response object passed in as method parameter, set cookie by `response.set_cookie(k, v)` without constructing response object

```python
@app.get("/cookie2", response_model=Result)
async def cookie2(response: Response, a: int, b: int):
    """_summary_

    Args:
        response (Response): response
        a (int): a
        b (int): b

    Returns:
        (Result)
    """
    response.set_cookie(
        key="_session_id",
        value="fake-session-id-2",
    )
    return Result(
        message="Hello World",
        code=200,
        data={
            "result": a + b,
        },
    )
```

### response header

- response header is a `Mapping[str, str]` actually, so the value cound be accessed just like dict by `response.headers[key]`, and so set header by `response.headers[key] = value`.
- two methods of getting response object is just like the above two methods in [`set cookie`](#set-cookie)

## Tortoise ORM

- in order to use `sqlmodel`, `pip install sqlmodel` to install it first.
- in order to use `tortoise`, `pip install tortoise-orm` to install it first.
- use `pip install tortoise-orm[asyncmy]` to install driver for mysql series database.(`asyncodbc` for sqlserver series database, `asyncpg`/`psycopg` for postgresql series database, `asyncmy`/`mysql` for mysql series database, `sqlite`/`aiosqlite` for sqlite series database)

### connection configuration

```python
async def init():
    # Initialize Tortoise ORM with MySQL database connection
    await Tortoise.init(
        db_url="mysql://root:password@127.0.0.1:13306/fastapi_dev",
        # Register models module - using __main__ for this example
        modules={"models": ["__main__"]},
    )

    # Generate database schemas based on defined models
    await Tortoise.generate_schemas(safe=True)
```

### model definition

```python
# Define User model that inherits from Tortoise's Model class
class User(Model):
    # Primary key field with auto increment
    id = IntField(
        pk=True,
        auto_increment=True,
        description="Primary key field with auto increment",
    )
    # Username field with maximum length of 255 characters and unique constraint
    username = CharField(
        max_length=255,
        unique=True,
        description="Username field with maximum length of 255 characters and unique constraint",
    )
    # Email field with maximum length of 255 characters and unique constraint
    email = CharField(
        max_length=255,
        unique=True,
    )
    # Password field with maximum length of 255 characters
    password = CharField(max_length=255)
    # Boolean field indicating if user is active, defaults to True
    is_active = BooleanField(default=True)
    # Boolean field indicating if user is superuser, defaults to False
    is_superuser = BooleanField(default=False)

    def __str__(self) -> str:
        return self.username

    class Meta:
        table = "users"  # Specify custom table name
```

#### model fields

- `IntField`: Integer field.
- `CharField`: String field.
- `TextField`: Text field.
- `BooleanField`: Boolean field.
- `FloatField`: Float field.
- `DecimalField`: Decimal field.
- `DateField`: Date field.
- `DateTimeField`: DateTime field.

### model relationship

- `ForeignKeyField`: Foreign key field.
- `OneToOneField`: One-to-one field.
- `ManyToManyField`: Many-to-many field.

#### ForeignKeyField
1. `ForeignKeyField` is used to define a relationship between two models.

    ```python
    class Order(Model):
        id = IntField(
            pk=True,
            auto_increment=True,
            description="Primary key field with auto increment",
        )
        order_number = CharField(
            max_length=100,
            unique=True,
            description="Order number with maximum length of 100 characters and unique constraint",
        )
        user = ForeignKeyField(
            "models.User",
            related_name="orders",
            description="Foreign key field to link to User model",
        )
        total_amount = IntField(
            description="Total amount for the order",
        )
        is_paid = BooleanField(default=False)

        def __str__(self) -> str:
            return self.order_number

        class Meta:
            table = "orders"  # Specify custom table name
            table_description = "Order table"  # Description for the table
    ```

    > in the example above, `ForeignKeyField("models.User", related_name="orders", description="")` is used to define a `one to many relationship` between `Order` model and `User` model.

2. reverse relation in `User` model

    ```python
    class User(Model):
        ...
        # reverse relation to Order model
        orders: ReverseRelation["Order"]
        ...
    ```

    > It is OK to only define `ReverseRelation` or `ForeignKeyField`

#### OneToOneField
```python
class UserInfo(Model):
    id = IntField(
        pk=True,
        auto_increment=True,
        description="Primary key field with auto increment",
    )
    user = OneToOneField(
        "models.User",
        related_name="userinfo",
        description="Foreign key field to link to User model",
    )
    ...
```
#### ManyToManyField
- `ManyToManyField` is used to define a many-to-many relationship between two models.
- the 'many-to-many' relationship will be stored in a separate table joins the primary key of the two models and could only by this way.

```python
# Many-to-Many relationship example
# Many-to-Many relationship example
class Group(Model):
    id = IntField(
        pk=True,
        auto_increment=True,
        description="Primary key field with auto increment",
    )
    name = CharField(
        max_length=100,
        unique=True,
        description="Group name with maximum length of 100 characters and unique constraint",
    )
    members = ManyToManyField(
        "models.User",
        related_name="groups",
        description="Many-to-Many relationship to User model",
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        table = "groups"  # Specify custom table name
        table_description = "Group table"  # Description for the table

```

#### Full Example
```python
from typing import Optional

from tortoise import (
    Tortoise,
    run_async,
    Model,
)
from tortoise.fields import (
    IntField,
    CharField,
    BooleanField,
    ForeignKeyField,
    ReverseRelation,
    OneToOneField,
    ManyToManyField,
)


# Define User model that inherits from Tortoise's Model class
class User(Model):
    # Primary key field with auto increment
    id = IntField(
        pk=True,
        auto_increment=True,
        description="Primary key field with auto increment",
    )
    # Username field with maximum length of 255 characters and unique constraint
    username = CharField(
        max_length=255,
        unique=True,
        description="Username field with maximum length of 255 characters and unique constraint",
    )
    # Email field with maximum length of 255 characters and unique constraint
    email = CharField(
        max_length=255,
        unique=True,
    )
    # Password field with maximum length of 255 characters
    password = CharField(max_length=255)
    # Boolean field indicating if user is active, defaults to True
    is_active = BooleanField(default=True)
    # Boolean field indicating if user is superuser, defaults to False
    is_superuser = BooleanField(default=False)
    # reverse relation to Other models
    orders: ReverseRelation["Order"]
    userinfo: ReverseRelation["UserInfo"]
    groups: ReverseRelation["Group"]

    def __str__(self) -> str:
        return self.username

    class Meta:
        table = "users"  # Specify custom table name
        table_description = "User table"  # Description for the table


# One-to-One relationship example
class UserInfo(Model):
    id = IntField(
        pk=True,
        auto_increment=True,
        description="Primary key field with auto increment",
    )
    user = OneToOneField(
        "models.User",
        related_name="userinfo",
        description="Foreign key field to link to User model",
    )
    full_name = CharField(
        max_length=255,
        description="Full name of the user",
    )
    address = CharField(
        max_length=500,
        description="Address of the user",
    )
    phone_number = CharField(
        max_length=20,
        description="Phone number of the user",
    )

    def __str__(self) -> str:
        return self.full_name

    class Meta:
        table = "user_info"  # Specify custom table name
        table_description = "User Info table"  # Description for the table


# Many-to-One relationship example
class Order(Model):
    id = IntField(
        pk=True,
        auto_increment=True,
        description="Primary key field with auto increment",
    )
    order_number = CharField(
        max_length=100,
        unique=True,
        description="Order number with maximum length of 100 characters and unique constraint",
    )
    user = ForeignKeyField(
        "models.User",
        related_name="orders",
        description="Foreign key field to link to User model",
    )
    total_amount = IntField(
        description="Total amount for the order",
    )
    is_paid = BooleanField(default=False)

    def __str__(self) -> str:
        return self.order_number

    class Meta:
        table = "orders"  # Specify custom table name
        table_description = "Order table"  # Description for the table


# Many-to-Many relationship example
class Group(Model):
    id = IntField(
        pk=True,
        auto_increment=True,
        description="Primary key field with auto increment",
    )
    name = CharField(
        max_length=100,
        unique=True,
        description="Group name with maximum length of 100 characters and unique constraint",
    )
    members = ManyToManyField(
        "models.User",
        related_name="groups",
        description="Many-to-Many relationship to User model",
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        table = "groups"  # Specify custom table name
        table_description = "Group table"  # Description for the table


async def init():
    # Initialize Tortoise ORM with MySQL database connection
    await Tortoise.init(
        db_url="mysql://root:password@127.0.0.1:13306/fastapi_dev",
        # Register models module - using __main__ for this example
        modules={"models": ["__main__"]},
    )

    # Generate database schemas based on defined models
    await Tortoise.generate_schemas(safe=True)


if __name__ == "__main__":
    # Run the async initialization function
    run_async(init())
    print("Database initialized and schemas generated.")
```

- equivalent SQL query:
```sql
CREATE TABLE `users` (
    `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Primary key field with auto increment',
    `username` varchar(255) NOT NULL COMMENT 'Username field with maximum length of 255 characters and unique constraint',
    `email` varchar(255) NOT NULL,
    `password` varchar(255) NOT NULL,
    `is_active` tinyint(1) NOT NULL DEFAULT 1,
    `is_superuser` tinyint(1) NOT NULL DEFAULT 0,
    PRIMARY KEY (`id`),
    UNIQUE KEY `username` (`username`),
    UNIQUE KEY `email` (`email`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_uca1400_ai_ci COMMENT = 'User table';

CREATE TABLE `user_info` (
    `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Primary key field with auto increment',
    `full_name` varchar(255) NOT NULL COMMENT 'Full name of the user',
    `address` varchar(500) NOT NULL COMMENT 'Address of the user',
    `phone_number` varchar(20) NOT NULL COMMENT 'Phone number of the user',
    `user_id` int(11) NOT NULL COMMENT 'Foreign key field to link to User model',
    PRIMARY KEY (`id`),
    UNIQUE KEY `user_id` (`user_id`),
    CONSTRAINT `fk_user_inf_users_f7a4c25a` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_uca1400_ai_ci COMMENT = 'User Info table';

CREATE TABLE `orders` (
    `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Primary key field with auto increment',
    `order_number` varchar(100) NOT NULL COMMENT 'Order number with maximum length of 100 characters and unique constraint',
    `total_amount` int(11) NOT NULL COMMENT 'Total amount for the order',
    `is_paid` tinyint(1) NOT NULL DEFAULT 0,
    `user_id` int(11) NOT NULL COMMENT 'Foreign key field to link to User model',
    PRIMARY KEY (`id`),
    UNIQUE KEY `order_number` (`order_number`),
    KEY `fk_orders_users_411bb784` (`user_id`),
    CONSTRAINT `fk_orders_users_411bb784` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_uca1400_ai_ci COMMENT = 'Order table';

CREATE TABLE `groups` (
    `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Primary key field with auto increment',
    `name` varchar(100) NOT NULL COMMENT 'Group name with maximum length of 100 characters and unique constraint',
    PRIMARY KEY (`id`),
    UNIQUE KEY `name` (`name`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_uca1400_ai_ci COMMENT = 'Group table';

CREATE TABLE `groups_users` (
    `groups_id` int(11) NOT NULL,
    `user_id` int(11) NOT NULL,
    UNIQUE KEY `uidx_groups_user_groups__403fc9` (`groups_id`, `user_id`),
    KEY `user_id` (`user_id`),
    CONSTRAINT `1` FOREIGN KEY (`groups_id`) REFERENCES `groups` (`id`) ON DELETE CASCADE,
    CONSTRAINT `2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_uca1400_ai_ci COMMENT = 'Many-to-Many relationship to User model';
```

### sql operations

#### Create user

- use `await User.create(username="xxx", email="xxx", ...)` to create a new user and auto insert into the database
- the auto-increment field will be automatically filled in

```python
async def do_create_user():
    # Example function to create a new user
    for i in range(5):
        user = await User.create(
            username=f"john_doe_{i}",
            email=f"john_doe_{i}@example.com",
            password="password",
        )
        print(f"Created user: {user}")
```

> However, the method `create` could be **error** if the unique constraint is violated when inserting. So, use `get_or_create` instead.

```python
async def do_create_user():
    # Example function to create a new user
    for i in range(5):
        user = await User.get_or_create(
            username=f"john_doe_{i}",
            email=f"john_doe_{i}@example.com",
            password="password",
        )
        print(f"Created user: {user}")
```


#### query users

- use `await User.all()` to query all users

```python
async def do_query_users():
    # Example function to query all users
    users = await User.all()
    for user in users:
        print(f"User: {user}, Email: {user.email}")
```

#### Update user

- use `user = User.get(key=value)` to specify the user to update
- use `user.update_from_dict(data)` to update the user with a dictionary of data
- change the fields to update
- save the changes by `user.save()`

```python
async def do_update_user():
    # Example function to update a user
    user = await User.get(username="john_doe_1")
    user.email = "john@example.com"
    await user.save()
    print(f"Updated user: {user}")
    user = await user.update_from_dict({"email": "john_doe_1@example.com"})
    await user.save()
    print(f"Updated user: {user}")
```

#### delete user

- use `user = User.get(key=value)` to specify the user to delete
- delete the user by `await user.delete()`

```python
async def do_delete_user():
    # Example function to delete a user
    user = await User.get(username="john_doe_1")
    await user.delete()
    print(f"Deleted user: {user}")
```

### Advanced Usage

> Use `User.get(key=value)` to query a single user, however, if there are multiple users with the same username or no users with the specified username, it will raise an error.

> To avoid error while no matched user by `get` method, use `get_or_none`.

#### filter

- `User.filter(key1=value1, key2=value2, ...)` will return a list of users that match the specified conditions

##### ambiguous conditions

```python
#  lt, gt, ...
users = await User.filter(age__gt=30)
print(f"Users older than 30: {users}")
users = await User.filter(age__lt=30)
print(f"Users younger than 30: {users}")
users = await User.filter(amount__gte=500)
print(f"Users with amount greater than or equal to 500: {users}")
users = await User.filter(amount__lte=300)
print(f"Users with amount less than or equal to 300: {users}")

# ambiguous query
users = await User.filter(age__gt=25, age__lt=35)
print(f"Users older than 25 and younger than 35: {users}")
users = await User.filter(age__range=(25, 35))
print(f"Users with age between 25 and 35: {users}")
```
##### LIKE conditions
```python
# contains, startwith...
users = await User.filter(email__contains="example.com")
print(f"Users with 'example.com' in email: {users}")
users = await User.filter(username__icontains="john")
print(f"Users with 'john' in username (case-insensitive): {users}")
users = await User.filter(username__startswith="john_doe_1")
print(f"Users with username starting with 'john_doe_1': {users}")
users = await User.filter(username__endswith="5")
print(f"Users with username ending with '5': {users}")
```

##### and conditions
- `User.filter(key1=value1, key2=value2, ...).update(key3=value3, ...)` will update the specified fields for all users that match the specified conditions

##### `update`
- `User.filter(is_active=True).update(is_superuser=False)` will update the specified fields for all active users

##### or conditions

```python
# OR conditions using Q objects
from tortoise.expressions import Q

users = await User.filter(Q(username="john") | Q(email="john@example.com"))
print(f"Users with username 'john' or email 'john@example.com': {users}")
```

##### `order_by`

- A '-' before the name will result in descending sort order, default is ascending.

```python
users = await User.all().order_by("-created_at")
print(f"Users ordered by creation date descending: {users}")
```

##### `limit` and `offset`

```python
# Limit results (pagination)
users = await User.all().limit(10).offset(20)
print(f"Users with limit and offset: {users}")
```

##### `count`

```python
# Count records
count = await User.filter(is_active=True).count()
print(f"Count of active users: {count}")
```

##### access related objects

```python
# Access related objects directly
user = await User.get(id=1)
orders = await user.orders.all()  # Get all orders for a user
print(f"Orders for user {user.username}: {orders}")

# Filter on related objects
paid_orders = await Order.filter(user__is_active=True, is_paid=True)
print(f"Paid orders for active users: {paid_orders}")
```

`Order` class has a `user` field which is a foreign key to the `User` model, and `User` class has a property named `is_active`. 
1. access related object directly: 
   - use `user.orders.all()` to get all orders for a user, but could not filter by conditions.
2. access related objects in filter:
   - use the `Order.user__is_active=True` which means `Order.user.is_active=True` in filter function to access related objects' property.

#### prefetch related objects

- use `prefetch_related` to optimize queries by prefetching related data.
- `prefetch_related` will fetch related data in a single query, which can improve performance.
- if not use `prefetch_related`, the access to related objects will trigger another query at first time of accessing related objects.

```python
# Optimize queries by prefetching related data
async def related_query():
    # Example function to demonstrate related queries
    # Fetch a user and their related orders and user info
    user = await User.get(username="john_doe_10").prefetch_related("orders", "userinfo")
    print(f"User: {user}")
    print(f"userinfo: {await user.userinfo}")
    print(f"Orders: {await user.orders.all()}")

    # Fetch an order and its related user
    order = await Order.get(order_number="ORDER_00010").prefetch_related("user")
    print(f"Order: {order}")
    print(f"Related User: {await order.user}")

    # Fetch a group and its members
    group = await Group.get(name="Group_1").prefetch_related("members")
    print(f"Group: {group}")
    print(f"Members: {await group.members.all()}")
```

#### `tortoise.functions`

Tortoise ORM provides built-in functions and aggregates for performing operations on database fields and calculating aggregated values across records.

##### Text Transformation Functions

Several functions are available for transforming text fields:

- `Trim("FIELD_NAME")` - Removes whitespace from both ends of text
- `Length("FIELD_NAME")` - Returns the character count of text/blob fields
- `Lower("FIELD_NAME")` - Converts text to lowercase
- `Upper("FIELD_NAME")` - Converts text to uppercase
- `Concat("FIELD_NAME", ANOTHER_FIELD_OR_TEXT)` - Combines fields or text values (note: not supported by all databases like SQLite)

##### Null Handling Functions

- `Coalesce("FIELD_NAME", DEFAULT_VALUE)` - Provides a fallback value when the field is NULL

##### Database-Specific Random Functions

Different databases have specific implementations for generating random numbers:
- MySQL: `Rand()`
- PostgreSQL: `Random()`
- SQLite: `Random()`

##### Aggregate Functions

Aggregates operate on entire columns and are typically used with grouping operations:

- `Count("FIELD_NAME")` - Counts the number of entries in a column
- `Sum("FIELD_NAME")` - Calculates the total sum of all values in a column
- `Max("FIELD_NAME")` - Finds the largest value in a column
- `Min("FIELD_NAME")` - Finds the smallest value in a column
- `Avg("FIELD_NAME")` - Computes the average (mean) of all values in a column

##### Example Usage
```python
# Add computed fields to queryset
from tortoise.functions import Count, Avg, Sum, Min, Max

# Group by example
order_group = (
    await Order.all()
    .annotate(total_orders=Count("id"))
    .group_by("user_id")
    # .values("user_id", "total_orders")
)
print(f"Order count grouped by user: {order_group}")

#  Count example
users_with_order_count = await User.annotate(order_count=Count("orders")).filter(
    order_count__gt=0
)
print(f"Users with at least one order: {users_with_order_count}")

# avg, min, max, sum examples
avg_age = await User.all().annotate(avg_age=Avg("age")).values("avg_age")
print(f"Average age of users: {avg_age}")
min_age = await User.all().annotate(min_age=Min("age")).values("min_age")
print(f"Minimum age of users: {min_age}")
max_age = await User.all().annotate(max_age=Max("age")).values("max_age")
print(f"Maximum age of users: {max_age}")
total_amount = (
    await User.all().annotate(total_amount=Sum("amount")).values("total_amount")
)
print(f"Total amount of users: {total_amount}")

```

##### Usage Patterns

Functions can be used in annotations and updates:

```python
# Using functions in annotations
from tortoise.functions import Upper, Length

users = await User.annotate(
    upper_name=Upper("username"),
    name_length=Length("username")
).all()

# Using custom functions
from pypika_tortoise import CustomFunction
from tortoise.expressions import F, Function

class TruncMonth(Function):
    database_func = CustomFunction("DATE_FORMAT", ["name", "dt_format"])

sql = Task.all().annotate(date=TruncMonth('created_at', '%Y-%m-%d')).values('date').sql()
print(sql)
# SELECT DATE_FORMAT(`created_at`,'%Y-%m-%d') `date` FROM `task`
```

- `CustomFunction` is a class that represents a custom function in SQL.
- `DATA_FORMAT` is the name of the function in SQL.
- `["name", "dt_format"]` is the list of arguments for the function `DATE_FORMAT`.
- So `TruncMonth('created_at', '%Y-%m-%d'))` is equal to `DATE_FORMAT(created_at,'%Y-%m-%d')` in SQL.

#### Execute raw SQL

```python
# Execute raw SQL when needed
users = await User.raw("SELECT * FROM users WHERE is_active = True")
print(f"Active users (raw SQL): {users}")
```

#### Transactions

##### `in_transaction`

```python
# Perform atomic operations
from tortoise.transactions import in_transaction

async with in_transaction() as connection:
    try:
        user = await User.create(
            username="transaction_user",
            email="transaction_user@example.com",
            password="password",
            age=30,
            amount=500,
            is_active=True,
            is_superuser=False,
        )
        await UserInfo.create(user=user, full_name="Test User")
    except Exception as e:
        await connection.rollback()
        print(f"Error creating user and user info in transaction: {e}")

print(f"Tried to create user and user info in transaction: {user}")
try:
    user = await User.get(username="transaction_user")
    print(f"Fetched user in transaction: {user}")
except Exception as e:
    print(f"Error fetching user in transaction: {e}")
# Both operations commit together or rollback together
```

##### `atomic`

`atomic` decorator can be used to wrap a function in a transaction.

```python
from tortoise.transactions import atomic

@atomic()
async def atomic_function():
    ...

try:
    await atomic_function()
except OperationalError:
    pass
```

#### execute raw SQL

```python
async def do_raw_sql():
    # Example function to execute raw SQL queries
    # Fetch users using raw SQL
    # query = "SELECT * FROM users WHERE id > 5"
    sql = "SELECT * FROM users WHERE id > %s"
    result = await Tortoise.get_connection("default").execute_query(sql, [95])
    print(f"Raw SQL query result size: {result[0]}")
    for idx, row in enumerate(result[1], 1):
        print(f"Raw SQL query result {idx}: {row}")
```

## Aerich

Aerich is a database migration tool for Tortoise ORM. It helps to manage database schema changes and keep track of them.

### Installation

> install aerich by `pip install aerich`

### Migration

> write config py file
```python
# aerich_test.py
from tortoise.contrib.fastapi import register_tortoise
from fastapi import FastAPI

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

register_tortoise(
    app,
    config=TORTOISE_ORM,
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="debug",
    )
```

> create migration file (do not create table in database)
```shell
❯ aerich init -t src.aerich_test.TORTOISE_ORM
Success writing aerich config to pyproject.toml
Success creating migrations folder ./migrations
```

> create tables in database

> !!! the database must be created before running this command or it will raise that could not connect to sql.

> <font color="red">DO NOT PUT `register_tortoise` IN CONDITION `if __name__ == "__main__":` or project might not registe it.</font>

```shell
❯ aerich init-db
Success creating app migration folder migrations/models
Success generating initial migration file for app "models"
Success writing schemas to database "aerich_test"
```

> now, the tables are created in database and the auto generated migration file is created in a py file in migrations/models, which includes the changes made to the database and the sql commands to execute those changes.

### Update Schema

> use `aerich migrate` to create the new migration file based the state in current migration file
```shell
❯ aerich migrate
Success creating migration file 1_20251219192230_update.py
```

> use `aerich upgrade` to update the schema
```shell
❯ aerich upgrade
Success upgrading to 1_20251219192230_update.py
```

## **APIRouter**

APIRouter is a class provided by FastAPI that allows you to group related routes together. It provides a way to organize your routes and make them easier to manage and maintain.

#### Usage

```python
from fastapi import APIRouter

router = APIRouter(
    prefix="/api/v1/admin",
    tags=["admin"],
    responses={
        404: {
            "description": "Not found",
        },
        403: {
            "description": "Forbidden",
        },
        401: {
            "description": "Unauthorized",
        },
    },
    dependencies=[Depends(token_validate)],
)
```
- `prefix`: A string that will be prepended to all the routes in this router.
- `tags`: A list of strings that will be used as tags for the routes in this router.
- `responses`: A dictionary that defines the responses for all the routes in this router.
- `dependencies`: A list of dependencies that will be applied to all the routes in this router.

#### Example

```python
# user_router.py
from fastapi import HTTPException, APIRouter

from models import UserModel
from schemas import LoginForm, RegisterForm, UserInfo

user_router_v1 = APIRouter(prefix="/api/v1/user")


@user_router_v1.post("/register", response_model=UserInfo)
async def register_user(item: RegisterForm):
    """Register a new user."""
    user = await UserModel.create(**item.model_dump(exclude={"password_confirm"}))
    return UserInfo.model_validate(user.__dict__)


@user_router_v1.post("/login", response_model=UserInfo)
async def login_user(item: LoginForm):
    """Login an existing user."""
    user = await UserModel.get_or_none(email=item.email, password=item.password)
    if not user:
        return HTTPException(status_code=400, detail="Invalid credentials")
    return UserInfo.model_validate(user.__dict__)
```

```python
# main.py
import uvicorn
from fastapi import FastAPI

from routes import user_router_v1

app = FastAPI()
app.include_router(user_router_v1)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
```

## Project Structure

### Layered Architecture (Most Common)


#### Core Configuration (core/)
+ config.py: Environment variables and settings management
+ security.py: Authentication, password hashing, JWT handling

#### Models and Schemas (models/, schemas/)
+ models/: Database ORM models (e.g., SQLAlchemy)
+ schemas/: Pydantic models for request/response validation

#### API Organization
+ Versioned APIs in separate directories
+ Routers organized by resource/entity
+ Dependency injection via deps.py

#### Data Access Layer
+ crud/: Create, Read, Update, Delete operations
+ Repository pattern for complex data access logic

```yaml
project/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Application entry point
│   ├── core/                   # Configuration and settings
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── security.py
│   ├── models/                 # Database models (SQLAlchemy)
│   │   ├── __init__.py
│   │   └── user.py
│   ├── schemas/                # Pydantic models for validation
│   │   ├── __init__.py
│   │   └── user.py
│   ├── api/                    # API routes and endpoints
│   │   ├── __init__.py
│   │   ├── deps.py             # Dependencies
│   │   ├── v1/                 # API version 1
│   │   │   ├── __init__.py
│   │   │   ├── routers/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── users.py
│   │   │   │   └── items.py
│   │   │   └── api.py          # API router aggregation
│   │   └── v2/                 # Future API version
│   ├── crud/                   # Database operations
│   │   ├── __init__.py
│   │   └── user.py
│   ├── utils/                  # Utility functions
│   │   ├── __init__.py
│   │   └── helpers.py
│   └── tests/                  # Test files
│       ├── __init__.py
│       ├── test_users.py
│       └── conftest.py
├── alembic/                    # Database migrations
├── requirements.txt
├── README.md
└── Dockerfile
```

### Feature-Based Structure (Advanced)
This approach groups code by features rather than technical layers:
```yaml
project/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── shared/                 # Shared components
│   │   ├── core/
│   │   ├── database/
│   │   └── security/
│   ├── users/                  # User feature module
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── service.py
│   │   ├── router.py
│   │   └── dependencies.py
│   ├── products/               # Product feature module
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── service.py
│   │   └── router.py
│   └── orders/                 # Order feature module
└── tests/
    ├── users/
    ├── products/
    └── orders/
```

### Domain-Driven Design (DDD) Approach
For complex applications with multiple bounded contexts:
```yaml
project/
├── src/
│   ├── __init__.py
│   ├── bootstrap.py            # Application initialization
│   ├── domain/                 # Business logic and entities
│   │   ├── __init__.py
│   │   ├── user/
│   │   └── order/
│   ├── application/            # Use cases and services
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   └── order_service.py
│   ├── infrastructure/         # External interfaces
│   │   ├── __init__.py
│   │   ├── database.py
│   │   ├── repositories.py
│   │   └── api_clients.py
│   └── presentation/           # API layer
│       ├── __init__.py
│       ├── fastapi_app.py
│       └── routers/
├── tests/
└── requirements.txt
```
## **Dependency Injection**

dependency injection is a design pattern that allows to decouple the dependencies of application.

### Function Dependency Injection

#### authorization validation
```python
async def verify_key(token: str = Header()):
    if token != "fake-super-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")

@app.get("/items/", dependencies=[Depends(verify_token),])
async def read_items(*_, **__):
    return {}

@app.get("/users/", dependencies=[Depends(verify_token),])
async def read_users(*_, **__):
    return {}
```

#### database connection and initialization
```python
def get_db():
    db = create_engine("postgresql://user:password@localhost/dbname")
    try:
        yield db
    finally:
        db.dispose()

@app.get("/features")
async def get_features(db = Depends(get_db)):
    # query database
    ...
    pass
```

#### log wreiting
```python
import logging

def log_request(request: Request):
    logging.info(f"Request to {request.url}")
    pass

@app.get("/xxx", dependencies=[Depends(log_request)])
async def xxx():
    # do something
    ...
    pass
```

#### Cache
```python
from cachetools import cached, TTLCache

@cached(cache=TTLCache(maxsize=100, ttl=300))
def get_cached_features():
    # get features from database
    pass

@app.get("/cached_features")
async def cached_features(features = Depends(get_cached_features)):
    return features
```

### Class Dependency Injection
```python
class CommonQueryParams:
    def __init__(self, q: Optional[str] = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit

@app.get("/items/")
async def read_items(commons: CommonQueryParams = Depends(CommonQueryParams)):
    return commons.__dict__

@app.get("/users/")
async def read_users(commons: CommonQueryParams = Depends(CommonQueryParams)):
    return commons.__dict__
```

### Sub-Dependency Injection
```python
def query_extractor(q: Optional[str] = None):
    return q

def query_or_cookie_extractor(
    q: str = Depends(query_extractor),
    last_query: Optional[str] = None,
):
    if not q:
        return last_query
    return q

@app.get("/items/")
async def read_query(query_or_default: str = Depends(query_or_cookie_extractor)):
    return {"q_or_default": query_or_default}
```

### Dependency Injection in Path
```python
async def verify_token(x_token: str = Header()):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")

async def verify_key(x_key: str = Header()):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")

@app.get("/items/", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items():
    return [{"item": "Portal Gun"}, {"item": "Plumbus"}]
```

### Global Dependency Injection
```python
async def verify_token(x_token: str = Header()):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")

async def verify_key(x_key: str = Header()):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")

# add to FastAPI application
app = FastAPI(dependencies=[Depends(verify_token), Depends(verify_key)])
```

## FastAPI Configuration

- **title**: The title of the API.
- **description**: A description of the API.
- **version**: The version of the API.
- **openapi_url**: The URL of the OpenAPI schema.
- **exception_handlers**: A dictionary of exception handlers.
- and so on ...

```python
app = FastAPI(
    title="FastAPI Study Note",
    description="FastAPI Study Note",
    version="0.1.0",
    openapi_url="/api/openapi.json",
    exception_handlers={},
)
```

## Global Exception Handler

### exception_handler decorator
```python
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    # custom handling for global parameters error
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": exc.detail,
            "code": exc.status_code,
            "data": None,
        },
    )
```

### add_exception_handler method
```python
...

from exceptions import http_exception_handler
from starlette.exceptions import HTTPException as StarletteHTTPException

app.add_exception_handler(StarletteHTTPException, http_exception_handler)
```

### custom exception

```python
# expeptions.py
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
            "tip": "要不要… 充个 10 块？"
        }
    )
```

```python
# main.py
from expeptions import InsufficientFundsError, insufficient_handler

app.add_exception_handler(InsufficientFundsError, insufficient_handler)

@app.post("/buy-coffee")
def buy_coffee(balance: float = 10.0) -> dict:
    price = 15.0
    if balance < price:
        raise InsufficientFundsError(balance, price)
    return {"msg": "☕ 已下单！老板说送你一块曲奇～"}

```

## FastAPI Middleware
- **CORS**: Cross-Origin Resource Sharing.  Cross-Origin Resource Sharing will happen when a frontend application tries to access a resource from a **different origin**.

- **different origin**: different protocol, host, or port. 

- Even though the same pc runs two web server, for example, a vue application served by nodejs and a fastapi application served by uvicorn, these two application will have different port, so, the two applications are considered to be different origins. 

- A html served by a fastapi could access the same fastapi backend by js method which could not be considered as cross-origin.

### Configuration in FastAPI
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# origins = [
#     "http://localhost.tiangolo.com",
#     "https://localhost.tiangolo.com",
#     "http://localhost",
#     "http://localhost:8080",
# ]

app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def main():
    return {"message": "Hello World"}
```

### Security Considerations

1. Restrict Origins Explicitly: Instead of allowing all origins ("*"), specify exact domains

2. Environment-Based Configuration: Use environment variables for flexible deployment
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# Read allowed origins from environment variable
ALLOWED_ORIGINS = os.getenv(
    "CORS_ALLOWED_ORIGINS", 
    "https://yourdomain.com"
).split(",")

# Remove any whitespace
ALLOWED_ORIGINS = [origin.strip() for origin in ALLOWED_ORIGINS]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=os.getenv("CORS_ALLOW_CREDENTIALS", "false").lower() == "true",
    allow_methods=os.getenv("CORS_ALLOWED_METHODS", "GET,POST,PUT,DELETE").split(","),
    allow_headers=os.getenv("CORS_ALLOWED_HEADERS", "Authorization,Content-Type").split(","),
    max_age=600,  # Cache preflight requests for 10 minutes
)
```
```bash
# .env
ENVIRONMENT=production
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
CORS_ALLOW_CREDENTIALS=false
CORS_ALLOWED_METHODS=GET,POST,PUT,DELETE
CORS_ALLOWED_HEADERS=Authorization,Content-Type,X-Requested-With
```

### **Custom Middleware**

- there is two ways to create custom middleware
  - by decorate a method with `@app.middleware("http")`
  - by creating a class which inherits from `BaseHTTPMiddleware` (starlette.middleware.base.BaseHTTPMiddleware) and override `dispatch` method. Then, add it to FastAPI application by `app.add_middleware(CustomCORSMiddleware)`

- **the two ways have no priority but the order of registration as middleware**.

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Method 1: Decorator
@app.middleware("http")
async def log_requests(request, call_next):
    print(f"Incoming request by method log_requests: {request.method} {request.url}")
    response = await call_next(request)
    print(f"Response status by method log_requests: {response.status_code}")
    return response

# Method 2: Class
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
```

#### CustomCORSMiddleware Class
- Dynamic Origin Validation: For more complex scenarios, validate origins dynamically

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import re


app = FastAPI()

class CustomCORSMiddleware(CORSMiddleware):
    def is_allowed_origin(self, origin: str) -> bool:
        """Check if origin is allowed based on pattern matching"""
        allowed_patterns = [
            r"^https://([a-zA-Z0-9-]+\.)*yourdomain\.com$",  # Main domain and subdomains
            r"^https://([a-zA-Z0-9-]+\.)*yourotherdomain\.com$",  # Additional domains
        ]
        
        # Allow localhost for development
        if os.getenv("ENVIRONMENT") == "development":
            allowed_patterns.append(r"^http://localhost:\d+$")
            allowed_patterns.append(r"^http://127\.0\.0\.1:\d+$")
        
        for pattern in allowed_patterns:
            if re.match(pattern, origin):
                return True
        return False

app.add_middleware(
    CustomCORSMiddleware,
    allow_origins=[],  # Empty list since we're using custom validation
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-Requested-With"],
    expose_headers=["Content-Disposition"],
    max_age=600,
)
```

#### internal advanced middleware in FastAPI
- `HTTPSRedirectMiddleware`: Redirects `HTTP` requests to `HTTPS` or `WS` requests to `WSS`
- `TrustedHostMiddleware`: Checks if the request's host is trusted
- `GZipMiddleware`: Compresses responses

```python
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware


app.add_middleware(GZipMiddleware, minimum_size=1000, compresslevel=5)
app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=["example.com", "*.example.com"]
)
app.add_middleware(HTTPSRedirectMiddleware)
```


### **Custom BaseHTTPMiddleware**

- Additional Security Measures

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
import os

app = FastAPI()

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # validate origin headers
        if not self.is_allowed_origin(request.headers.get("origin")):  # Custom method
            raise HTTPException(status_code=403, detail="Invalid origin")

        response = await call_next(request)
        
        # Additional security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        return response

# Apply security headers middleware
app.add_middleware(SecurityHeadersMiddleware)

# Restricted CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ALLOWED_ORIGINS", "").split(",") if os.getenv("CORS_ALLOWED_ORIGINS") else [],
    allow_credentials=False,  # Disable unless absolutely necessary
    allow_methods=["GET"],  # Minimal required methods
    allow_headers=["Content-Type"],  # Minimal required headers
    max_age=3600,  # Longer caching for production
)
```

## **Background Tasks**

To explain the background task in FastAPI, i wrote a email verification code demo.

### Demo Config

> This part stored the configuration of redis and RabbitMQ, and settings of this demo.

```python
import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    redis_host: str = os.getenv("REDIS_HOST", "localhost")
    redis_port: int = int(os.getenv("REDIS_PORT", 6379))
    redis_password: str = os.getenv("REDIS_PASSWORD", "")

    rabbitmq_host: str = os.getenv("RABBITMQ_HOST", "localhost")
    rabbitmq_port: int = int(os.getenv("RABBITMQ_PORT", 5672))
    rabbitmq_username: str = os.getenv("RABBITMQ_USERNAME", "admin")
    rabbitmq_password: str = os.getenv("RABBITMQ_PASSWORD", "password")

    # 验证码相关设置
    verification_code_length: int = 6
    verification_code_expire_seconds: int = 300  # 5分钟过期


settings = Settings() # Singoton
```

### Email service

> This part handles the code generation, the email sending function, and the callback function of email sending message from MessageQueue.

```python
import random
import string
from redis_client import redis_client
import json


from message_queue import message_queue


def generate_verification_code(length: int = 6) -> str:
    """生成验证码"""
    return "".join(random.choices(string.digits, k=length))


def send_verification_code(email: str, code: str):
    """发送验证邮件的模拟实现"""
    print(f"Sending verification code {code} to {email}")
    # 这里可以集成真实的邮件发送服务
    # 例如：smtplib, sendgrid, 或其他邮件服务

    # 模拟邮件发送过程
    import time
    import random
    import rich.progress

    with rich.progress.Progress() as progress:
        task = progress.add_task(f"[green]Sending email to {email}...", total=100)
        while not progress.finished:
            progress.update(task, advance=random.randint(5, 15))
            time.sleep(0.5)

    print(f"Verification code {code} sent successfully to {email}")


def process_email_task(ch, method, properties, body):
    """处理邮件任务的回调函数"""
    try:
        data = json.loads(body)
        email = data.get("email")
        code = data.get("code")

        # 发送邮件
        send_verification_code(email, code)

        # 手动确认消息已处理
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"Error processing email task: {e}")
        # 拒绝消息并重新入队
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)


def request_verification_code(email: str) -> str:
    """请求验证码"""
    code = generate_verification_code()

    # 存储验证码到Redis
    success = redis_client.set_verification_code(email, code)

    if success:
        message_queue.publish_email_task(email, code)
        print(f"Published email task for {email} with code {code}")
        return code
    else:
        raise Exception("Failed to store verification code in Redis")
```
- `send_verification_code` is a function that simulates the process of sending an email with a verification code.
- `process_email_task` is a callback function that processes the email task from the message queue (see `MessageQueue.consume_email_tasks` and `email_consumer.py` for details)
  - `ch.basic_ack` is used to manually confirm that the message has been processed.
  - `ch.basic_nack` is used to manually reject the message and requeue it.
- `request_verification_code` could generate a verification code and store it in Redis, then publish to the RabbitMQ.
- <font color=red>**!!!** In the Whole Demo, the email code will be print only in function `send_verification_code` to simulate the email sending process.</font> So, only if the process of virtual email sending is successful, the verification code will be print.


### Redis Client

> This part handles the redis connection and the verification code storage.

```python
import redis
import json
from typing import Optional
from config import settings


class RedisClient:
    def __init__(self):
        self.client = redis.Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            password=settings.redis_password,
            decode_responses=True,
            db=0,
        )

    def set_verification_code(self, email: str, code: str) -> bool:
        """存储验证码到Redis"""
        try:
            key = f"verification_code:{email}"
            # 验证码5分钟过期
            result = self.client.setex(
                name=key, time=settings.verification_code_expire_seconds, value=code
            )
            return result
        except Exception as e:
            print(f"Error setting verification code: {e}")
            return False

    def get_verification_code(self, email: str) -> Optional[str]:
        """从Redis获取验证码"""
        try:
            key = f"verification_code:{email}"
            code = self.client.get(key)
            return code
        except Exception as e:
            print(f"Error getting verification code: {e}")
            return None

    def delete_verification_code(self, email: str) -> bool:
        """删除验证码"""
        try:
            key = f"verification_code:{email}"
            result = self.client.delete(key)
            return result > 0
        except Exception as e:
            print(f"Error deleting verification code: {e}")
            return False


redis_client = RedisClient()

if __name__ == "__main__":
    # 测试Redis连接和方法
    rc = RedisClient()
    test_email = "test@example.com"
    test_code = "123456"
    rc.set_verification_code(test_email, test_code)
    retrieved_code = rc.get_verification_code(test_email)
    print(f"Retrieved code: {retrieved_code}")
    rc.delete_verification_code(test_email)
    deleted_code = rc.get_verification_code(test_email)
    print(f"Code after deletion: {deleted_code}")
```

- `RedisClient` is a very simple Redis client with basic functions for coding verification.
  - `setex` means set with expiration time while `setnx` means set if not exists in redis.
  - `.get` is used to get the value of a key in redis while `.getdel` is used to get and delete a key in redis, `.getdel` could not be used for the key user request could not match and verification code in redis will still be available.
  - `.delete` is used to delete a key in redis.

### Message Queue

> This part handles the message queue connection and the email task publishing to RabbitMQ.

```python
import pika
import json
from typing import Dict, Any
from config import settings


class MessageQueue:

    def __init__(self):
        self.init()

    def __enter__(self):
        self.init()
        return self

    def init(self):
        self.connection = None
        self.channel = None
        """连接到RabbitMQ"""
        try:
            credentials = pika.PlainCredentials(
                settings.rabbitmq_username, settings.rabbitmq_password
            )
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=settings.rabbitmq_host,
                    port=settings.rabbitmq_port,
                    credentials=credentials,
                )
            )
            self.channel = self.connection.channel()

            # 声明邮件队列
            self.channel.queue_declare(queue="email_verification_queue", durable=True)

        except Exception as e:
            print(f"Error connecting to RabbitMQ: {e}")
        assert self.connection and self.channel, "Failed to connect to RabbitMQ"

    def publish_email_task(self, email: str, code: str):
        """发布邮件发送任务到队列"""
        try:
            message = {"email": email, "code": code, "timestamp": self.get_timestamp()}

            self.channel.basic_publish(
                exchange="",
                routing_key="email_verification_queue",
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # 消息持久化
                ),
            )
            print(f"Email task published for {email}")
        except Exception as e:
            print(f"Error publishing email task: {e}")
            import traceback

            traceback.print_exc()

    def consume_email_tasks(self, callback_func):
        """消费邮件任务"""
        try:
            # 设置QoS，一次只处理一个消息
            self.channel.basic_qos(prefetch_count=1)

            self.channel.basic_consume(
                queue="email_verification_queue", on_message_callback=callback_func
            )

            print("Waiting for email tasks. To exit press CTRL+C")
            self.channel.start_consuming()
        except Exception as e:
            print(f"Error consuming email tasks: {e}")

    def get_timestamp(self):
        from datetime import datetime

        return datetime.now().isoformat()

    def __exit__(self, exc_type, exc_value, traceback):
        if self.connection and not self.connection.is_closed:
            self.connection.close()


message_queue = MessageQueue()

if __name__ == "__main__":
    # 测试连接和发布消息
    with MessageQueue() as mq:
        # mq.publish_email_task("test@example.com", "123456")
        mq.consume_email_tasks(
            lambda ch, method, properties, body: print(f"Received: {body}")
        )
```

- `consume_email_tasks` is a method that will always be called when a message is received from the queue, and always be waiting for new messages, so there would be no end point.
  - `basic_consume` set callback function to handle new messages.
  - `basic_qos` set QoS to 1, which means only one message will be processed at a time.
  - `start_consuming` will start consuming messages and wait for new messages **which will never be ended**.
- `publish_email_task` is a method that publishes a message to the queue with the email and verification code.
  - `basic_publish` sends a message to the queue, `exchange` is empty, which means the message will be sent to the default exchange, `routing_key` is the queue name, `body` is the message body, `properties` is the message properties, `delivery_mode` is 2, which means the message will be persisted, "2" is the delivery mode which be `Transient` when value is `1` and be `Persistent` when value is `2`.

### FastAPI Server

> This part handles the FastAPI server and the email verification process.

```python
from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel, EmailStr
from redis_client import redis_client
from email_service import request_verification_code
import json

app = FastAPI()


class EmailRequest(BaseModel):
    email: EmailStr


@app.post("/send_code/")
async def send_verification_code(
    request: EmailRequest, background_tasks: BackgroundTasks
):
    """发送验证码到邮箱"""
    try:
        background_tasks.add_task(request_verification_code, request.email)
        print(f"Scheduled background task to send code to {request.email}")
        return {
            "message": "Verification code has being sent in the background.",
            "email": request.email,
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to send verification code: {str(e)}"
        )


@app.post("/verify_code/")
async def verify_code(email: str, code: str):
    """验证验证码"""
    stored_code = redis_client.get_verification_code(email)

    if stored_code and stored_code == code:
        # 验证成功后删除验证码
        redis_client.delete_verification_code(email)
        return {"message": "Verification successful"}
    else:
        raise HTTPException(
            status_code=400, detail="Invalid or expired verification code"
        )


@app.get("/health")
async def health_check():
    """健康检查"""
    try:
        # 测试Redis连接
        redis_client.client.ping()

        return {
            "status": "healthy",
            "services": ["redis", "rabbitmq"],
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service unavailable: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
    )
```

- in `send_code` route, the background task is scheduled to send the verification code to the email, and directly returns a "email has been sent" result to the user without waiting for the result of email, redis and RabbitMQ components.
- `verify_code` route is used to verify the verification code, and the verification code is retrieved from redis. code will be get by function  `redis_client.get_verification_code` and compared in FastAPI function. If matched, the verification code will be invalid and will be deleted from redis by function `redis_client.delete_verification_code`.

### Email Consumer

> This part handles the email consumer service.

```python
import json
import pika
from message_queue import message_queue
from email_service import process_email_task

if __name__ == "__main__":
    try:
        # 启动邮件消费者服务
        message_queue.consume_email_tasks(process_email_task)
    except KeyboardInterrupt:
        print("Email consumer stopped by user")
```

- `message_queue.consume_email_tasks` is a callback function that processes the email task.
- If there is no message in the queue, the consumer will wait for a new message; if there is a message in the queue, the consumer will process it. (See the `MessageQueue.consume_email_tasks` function for details)


### docker compose file

> Settings of ports, username and password should be the same as in the config.py file.

```yaml
version: '3.8'

services:
  redis:
    image: redis:latest
    container_name: redis-mail-verification
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes

  rabbitmq:
    image: rabbitmq:management-alpine
    container_name: rabbitmq-mail-verification
    ports:
      - "5672:5672"
      - "15672:15672"
    environment:
      RABBITMQ_DEFAULT_USER: admin
      RABBITMQ_DEFAULT_PASS: password
    volumes:
      - rabbitmq_data:/var/lib/rabbitmq

volumes:
  redis_data:
  rabbitmq_data:
```

### Run Demo

1. create a redis and RabbitMQ instance in docker by command: `docker compose up -d`
2. run email consumer: `python email_consumer.py`
3. run fastapi server: `python main.py`

## WebSockets Demo

To use `WebSockets` in FastAPI, websockets should be installed by `pip install websockets`.

```python
# FastAPI WebSockets Demo

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List
import asyncio
from pydantic import BaseModel
import random

app = FastAPI()


class WsMessage(BaseModel):
    message: str
    code: int
    user_id: int


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    def __enter__(self):
        self.__init__()
        return self

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_str_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def send_json_message(self, data: dict, websocket: WebSocket):
        await websocket.send_json(data)

    async def send(self, websocket: WebSocket, message: WsMessage):
        await websocket.send_json(message.model_dump())

    async def broadcast_str(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    async def broadcast_json(self, data: dict):
        for connection in self.active_connections:
            await connection.send_json(data)

    async def broadcast(self, message: WsMessage):
        for connection in self.active_connections:
            await connection.send_json(message.model_dump())

    def __exit__(self, exc_type, exc_value, traceback):
        for connection in self.active_connections:
            try:
                asyncio.create_task(connection.close())
            except Exception as e:
                print(f"Error closing connection: {e}")


manager = ConnectionManager()


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            if data.lower() == "bye~~":
                await manager.send_str_message("bye~~", websocket)
                manager.disconnect(websocket)
                break
            print(f"[Server] Received from Client #{client_id}: {data}")
            await manager.send_str_message(f"You wrote: {data}", websocket)
            await manager.send_json_message(
                {"message": f"You wrote: {data}"}, websocket
            )
            await manager.send(
                websocket,
                WsMessage(
                    message=f"Hello Client #{client_id}, you sent: {data}",
                    code=200,
                    user_id=client_id,
                ),
            )
            await manager.send(
                websocket,
                WsMessage(
                    message=f"seed : {random.randint(1000,9999)}",
                    code=200,
                    user_id=client_id,
                ),
            )
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(
            WsMessage(
                message=f"Client #{client_id} disconnected",
                code=1001,
                user_id=client_id,
            )
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
    )
```

- `async def websocket_endpoint(websocket: WebSocket, client_id: int)` to handle websocket connection.
- `@app.websocket("/ws/{client_id}")` to register the websocket route.
- `websocket`
  - `.accept()` to accept the websocket connection, once this method is called, the websocket connection will be established.
  - `.send_deninal_response()` to send a denial (deny) response to the client. (usually used when the client is not authorized to access the websocket)
  - `.receive_text()` to receive text message from the client.
  - `.receive_json()` to receive json message from the client.
  - `.receive_bytes()` to receive bytes message from the client.
  - `.send_text()` to send text message to the client.
  - `.send_json()` to send json message to the client.
  - `.send_bytes()` to send bytes message to the client.
  - `.iter_text()` to iterate over text messages from the client.
  - `.iter_json()` to iterate over json messages from the client.
  - `.iter_bytes()` to iterate over bytes messages from the client.
  - `.close()` to close the websocket connection.
  - `.application_state` to get the application state.
    - `WebSocketState.RESPONSE`(=3) to check if the websocket is in response state.
    - `WebSocketState.DISCONNECTED`(=2) Connection closed.
    - `WebSocketState.CONNECTED`(=1) Connection established and ready for send/receive.
    - `WebSocketState.CONNECTING`(=0) Handshake in progress.

## OAuth2.0

### passlib

> `passlib` is a Python library for password hashing and verification. It provides a simple, yet secure way to store and verify passwords.

- `pip install passlib` to install passlib
- to use "argon2", use `pip install "passlib[argon2]"` to install backend

#### Usage

```python
# pass_util.py
from passlib.context import CryptContext
from passlib.hash import sha256_crypt, pbkdf2_sha256, scrypt, argon2

algorithms = {
    "sha256_crypt": sha256_crypt,
    "pbkdf2_sha256": pbkdf2_sha256,
    "scrypt": scrypt,
    "argon2": argon2,
}

pwd_context = {a: CryptContext(schemes=[a], deprecated="auto") for a in algorithms}


async def verify_password(plain_password, hashed_password):
    for a in algorithms:
        if pwd_context[a].verify(plain_password, hashed_password):
            return True
    return False


async def get_password_hash(password, algorithm="sha256_crypt"):
    if algorithm in algorithms:
        return pwd_context[algorithm].hash(password)
    raise ValueError(f"Unsupported algorithm: {algorithm}")


if __name__ == "__main__":
    from pprint import pprint

    password = "123456789"
    hashed_password = {a: pwd_context[a].hash(password) for a in algorithms}
    pprint("Hashed password:")
    pprint(hashed_password)

    verification_results = {
        a: pwd_context[a].verify(password, hashed_password[a]) for a in algorithms
    }
    pprint("Verification results:")
    pprint(verification_results)
```

- `ctx = CryptContext(schemes=["sha256_crypt"], deprecated="auto")` to create a CryptContext object, while "sha256_crypt" is a algorithm.
- `hashed = ctx.hash(password)` to hash a password using the specified algorithm.
- `ctx.verify(password, hashed)` to verify a password against a hashed password.

### JWT (JSON Web Token)

> JSON Web Token (JWT) is an open standard (RFC 7519) that defines a compact and self-contained way for securely transmitting information between parties as a JSON object. It is commonly used for authentication and authorization purposes.

- a JWT string consists of three parts separated by dots (.), which are:
  - Header: A JSON object that describes the **type** of token and the **signing algorithm type** used. The Header is encoded in base64 and concat with a dot (.) and then the Payload.
  - Payload: A JSON object that contains the claims. The Payload is encoded in base64 and concat with a dot (.) and then the Signature.
    - iss: The issuer of the token.
    - sub: The subject of the tdoken.
    - aud: The audience of the token.
    - exp: The expiration time of the token.
    - at: The time when the token was issued.
  - Signature: A cryptographic signature that verifies the integrity of the token. The Signature is created using the former encoded part (Header and Payload), and a secret key, encoding in the algorithm specified in the Header, which is to ensure the whole JWT is tamper-proof.

#### Usage
```python
import jwt
import time
import tqdm

# import secrets

# print(secrets.token_hex(32))
# exit(0)

SECURITY_ALGORITHM = "HS256"
SECURITY_KEY = "e3c56abd1523a8fd4b73da842c272d1cf8a42acc78aafbd18890daaa2feb4755"


def generate_jwt(payload, secret=SECURITY_KEY, algorithm="HS256", expires_in=None):
    if expires_in is not None:

        payload["exp"] = datetime.datetime.now(datetime.UTC) + datetime.timedelta(
            seconds=expires_in
        )
    token = jwt.encode(
        payload,
        secret,
        algorithm=algorithm,
    )
    return token


def decode_jwt(token, secret=SECURITY_KEY, algorithms=["HS256"]):
    try:
        decoded = jwt.decode(token, secret, algorithms=algorithms)
        return decoded
    except jwt.ExpiredSignatureError:
        return "Token has expired"
    except jwt.InvalidTokenError:
        return "Invalid token"


if __name__ == "__main__":
    # generate a sample JWT
    sample_payload = {"user_id": 123, "role": "admin"}
    token = generate_jwt(
        sample_payload,
        expires_in=2,  # token expires in 5 seconds
    )
    print("Generated JWT:")
    print(token)

    # decode the sample JWT
    decoded_payload = decode_jwt(token)
    print("[Result] Decoded JWT payload:", decoded_payload)
    print("[Result] Decoded with wrong key:", decode_jwt(token, secret="wrongkey"))
    print("* Decoded with expired token:")
    for _ in tqdm.tqdm(range(3), desc="Waiting for token to expire"):
        time.sleep(1)  # wait for token to expire
    print("[Result] ", decode_jwt(token))
```
- `jwt.encode(payload, secret, algorithm="HS256")` to encode a payload into a JWT string.
- `jwt.decode(token, secret, algorithms=["HS256"])` to decode a JWT string into a payload.
- `jwt.ExpiredSignatureError` to catch expired token.
- `jwt.InvalidTokenError` to catch invalid token.

- set expire time: set key `exp` in payload with a deadline timestamp or datetime object **in UTC**

### OAuth2.0 in FastAPI

#### OAuth2PasswordBearer

> `OAuth2PasswordBearer` used as dependency to get a valid access token from the request.

```python
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    pass
```

#### Theory of OAuth2.0

- user token (user name or id) is stored in the payload of JWT
- the secret key is only stored in the server
- if the JWT token is invalid, the server could not decode the JWT or could not get the user token correctly
- JWT could store expire time too

1. the client passes a valid JWT to the server
2. the server decodes the JWT using the secret key and get the user token from the payload

```python
async def get_current_user(
    security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme)]
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        scope: str = payload.get("scope", "")
        token_scopes = scope.split(" ")
        token_data = TokenData(scopes=token_scopes, username=username)
    except (InvalidTokenError, ValidationError):
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user
```

#### OAuth2.0 Demo

##### main

```python
# main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.params import Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

from sqlite_util import (
    create_user,
    authenticate_user,
    TORTOISE_ORM,
    get_user_by_id,
)
from jwt_util import create_access_token, decode_jwt
from tortoise.contrib.fastapi import register_tortoise

app = FastAPI()

register_tortoise(
    app,
    config=TORTOISE_ORM,
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.post("/users/register")
async def signup(username: str, email: str, password: str):
    user = await create_user(username, email, password)
    if not user:
        raise HTTPException(status_code=400, detail="email already registered")
    oauth2_token = create_access_token(
        data={
            "sub": user.id,
        },
    )
    return {"access_token": oauth2_token, "token_type": "bearer"}


@app.post("/users/login")
async def login(
    email: str = Form(..., alias="mail"), password: str = Form(..., alias="pwd")
):
    # Dummy login logic for demonstration
    user = await authenticate_user(email, password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    oauth2_token = create_access_token(
        data={
            "user_id": user.id,
        },
    )
    return {"access_token": oauth2_token, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_jwt(token)
        print("Decoded JWT payload:", payload)
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = await get_user_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
    )

```

> `login` will verify user with password, and create a token include user_id for user if user password is valid.

> `read_users_me` will get bearer token by `Depends(oauth2_scheme)`, and decode it by `decode_jwt(token)` to get user_id.

##### sqlite util
```python
# sqlite client and schema

from tortoise import Tortoise, Model
from tortoise.fields import CharField, IntField, BooleanField

from pass_util import get_password_hash, verify_password

TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.sqlite",
            "credentials": {"file_path": "db.sqlite3"},
        },
    },
    "apps": {
        "models": {
            "models": ["aerich.models", "sqlite_util"],
            "default_connection": "default",
        },
    },
}


################### User Schema ###################


class User(Model):
    id = IntField(
        pk=True,
        auto_increment=True,
        description="id of user",
    )
    username = CharField(
        max_length=255,
        description="username of user",
    )
    email = CharField(
        max_length=255,
        description="email of user",
    )
    password_hash = CharField(
        max_length=255,
        description="hashed password of user",
    )
    is_active = BooleanField(
        default=True,
        description="is user active",
    )


################### User Service ###################


async def create_user(username, email, password):
    if await User.get_or_none(email=email):
        return None
    user = await User.create(
        username=username,
        email=email,
        password_hash=await get_password_hash(password),
    )
    return user


async def authenticate_user(email: str, password: str):
    user = await User.get_or_none(email=email)
    if not user:
        return None
    if not await verify_password(password, user.password_hash):
        return None
    return user


async def get_user_by_id(id: int):
    user = await User.get_or_none(id=id)
    return user
```

##### jwt util

```python
import jwt
import time
import tqdm
import json
from datetime import datetime, timedelta, timezone

# import secrets

# print(secrets.token_hex(32))
# exit(0)

SECURITY_ALGORITHM = "HS256"
SECURITY_KEY = "e3c56abd1523a8fd4b73da842c272d1cf8a42acc78aafbd18890daaa2feb4755"


def generate_jwt(payload, secret=SECURITY_KEY, algorithm="HS256", expires_in=None):
    if expires_in is not None:
        import datetime

        payload["exp"] = datetime.datetime.now(datetime.UTC) + datetime.timedelta(
            seconds=expires_in
        )
    token = jwt.encode(
        payload,
        secret,
        algorithm=algorithm,
    )
    return token


def decode_jwt(token, secret=SECURITY_KEY, algorithms=["HS256"]):
    try:
        decoded = jwt.decode(token, secret, algorithms=algorithms)
        return decoded
    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")


def create_access_token(
    data: dict, expires_delta: timedelta | None = timedelta(seconds=60 * 60 * 24)
):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECURITY_KEY, algorithm=SECURITY_ALGORITHM)
    return encoded_jwt
```

## Asyncio

### 主要概念

- `event_Loop`(イベントループ): すべての asyncio アプリケーションの核となるもので、非同期タスクの管理と実行を行う
- `Coroutine`(コルーチン): 時停止および再開可能な特別な関数（async def で定義）
- `Task`: 行実行するためにコルーチンをラップしたオブジェクト
- `Future`: 非同期操作の結果を表すオブジェクト

### Basic Usage

```python
import asyncio

async def my_function():
    await asyncio.sleep(1)  # Non-blocking sleep
    return "Hello from coroutine"

# Running the coroutine
asyncio.run(my_function())
```

- `asyncio.run()`: タスクを実行するためのメイン関数
- `async def`: タスクを定義するためのキーワード
- `await`: タスクを実行するためのキーワ
- `asyncio.sleep()`: タスクを実行するための非同期関数, `time.sleep()` はブロッキング関数ので、タスクを実行するためには `asyncio.sleep()` を使用する必要があります。

### event_Loop

`event_Loop` は、複数のタスクを並行する管理者である。

```python
loop = asyncio.get_event_loop()
loop.run_until_complete(my_function())
loop.run_in_executor(None, sync_func, *args)
```

- `asyncio.get_event_loop()` は、現在のスレッドで実行されているイベントループを取得する、もし存在しなければ新たに作成する。
- `loop.run_until_complete(my_function())` は、`my_function()` を実行し、その結果を待つ。<font color="red">**注意**: `my_function`は非同期関数でなければならない。</font>
- `loop.run_in_executor(None, sync_func, *args)` は、`sync_func` を実行し、その結果を待つ。<font color="red">**注意**: `sync_func`は同期関数でなければならない。</font>

### Task

> Tasks are used to schedule coroutines concurrently.

> When a coroutine is wrapped into a `Task` with function `asyncio.create_task()`, it is executed asynchronously on the event loop, scheduled to run soon.

```python
import asyncio
from loguru import logger


_LOOP = asyncio.get_event_loop()


async def my_function(id=0):
    logger.debug(f"id[{id}]: Hello from my_function")
    await asyncio.sleep(1)
    logger.debug(f"id[{id}]: Goodbye from my_function")
    return f"id:{id} is done"


async def main():

    await my_function(2)

    task = asyncio.create_task(my_function(3))  # python 3.7+

    # await asyncio.sleep(2)

    await task

    task_list = [asyncio.create_task(my_function(i)) for i in range(4, 7)]
    done, pedding = await asyncio.wait(task_list, timeout=10)
    for task in done:
        logger.debug(task.result())

    task_list = [asyncio.create_task(my_function(i)) for i in range(4, 7)]
    results = await asyncio.gather(*task_list)
    for result in results:
        logger.debug(result)


if __name__ == "__main__":
    _LOOP.run_until_complete(my_function(1))
    asyncio.run(main())
```

result:
```shell
__main__:my_function:9 - id[1]: Hello from my_function
__main__:my_function:11 - id[1]: Goodbye from my_function
__main__:my_function:9 - id[2]: Hello from my_function
__main__:my_function:11 - id[2]: Goodbye from my_function
__main__:my_function:9 - id[3]: Hello from my_function
__main__:my_function:11 - id[3]: Goodbye from my_function
__main__:my_function:9 - id[4]: Hello from my_function
__main__:my_function:9 - id[5]: Hello from my_function
__main__:my_function:9 - id[6]: Hello from my_function
__main__:my_function:11 - id[4]: Goodbye from my_function
__main__:my_function:11 - id[5]: Goodbye from my_function
__main__:my_function:11 - id[6]: Goodbye from my_function
__main__:main:28 - id:4 is done
__main__:main:28 - id:6 is done
__main__:main:28 - id:5 is done
__main__:my_function:9 - id[4]: Hello from my_function
__main__:my_function:9 - id[5]: Hello from my_function
__main__:my_function:9 - id[6]: Hello from my_function
__main__:my_function:11 - id[4]: Goodbye from my_function
__main__:my_function:11 - id[5]: Goodbye from my_function
__main__:my_function:11 - id[6]: Goodbye from my_function
__main__:main:33 - id:4 is done
__main__:main:33 - id:5 is done
__main__:main:33 - id:6 is done
```

## Future

> A `Future` is a special low-level object that represents an eventual result of an asynchronous operation.

つまり、`Future` は非同期操作の結果を表す特殊な低レベルオブジェクトである。


```python
loop = asyncio.get_running_loop()
logger.debug(f"loop == _LOOP: {loop == _LOOP}")  # False

fut = loop.create_future()
fut.set_result("done")
result = await fut
logger.debug(result)

fut = loop.run_in_executor(None, sync_func, 1)
logger.debug(f"fut: {fut}")
result = await fut
logger.debug(result)
```