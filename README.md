# fastapi_study_note

このノートでは、FastAPIを使って、APIを書く方法を学んでいきます。

## Installation

`pip install fastapi` でインストールします。
`pip install "uvicorn[standard]"` で、Uvicorn server もインストールします。

## pydantic

pydanticは、Pythonの型チェックを行うライブラリです。

```python
from pydantic import BaseModel


class TestModel(BaseModel):
    id: int
    name: str
    age: int


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

