# fastapi_study_note

このノートでは、FastAPIを使って、APIを書く方法を学んでいきます。

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


## fastapi request parameters

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

