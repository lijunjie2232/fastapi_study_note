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
```

> create migration file (do not create table in database)
```shell
❯ aerich init -t src.aerich_test.TORTOISE_ORM
Success writing aerich config to pyproject.toml
Success creating migrations folder ./migrations
```

> create tables in database

> !!! the database must be created before running this command or it will raise that could not connect to sql.

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

1. usage of authorization token validation
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

2. usage of database connection
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


