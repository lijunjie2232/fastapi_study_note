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