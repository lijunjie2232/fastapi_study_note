from pydantic import BaseModel
from pprint import pprint as print


class TestModel(BaseModel):
    id: int
    name: str
    age: int = 0  # デフォルト値


class MessageModel(BaseModel):
    message: str
    success: bool
    data: dict


def print_test_model(model: TestModel):
    print(model)


if __name__ == "__main__":
    test_model = TestModel(
        id=1,
        name="Alice",
        age=30,
    )
    print_test_model(test_model)
    # id=1 name='Alice' age=30

    msg = MessageModel(
        message="Success",
        success=True,
        data={
            "users": [],
        },
    )
    print(msg)
    # message='Success' success=True data={'users': []}

    test_model2 = TestModel(
        id="2",
        name="Bob",
        age="25",
    )
    print_test_model(test_model2)
    # id=2 name='Bob' age=25

    print(test_model2.model_dump())
    # {'id': 2, 'name': 'Bob', 'age': 25}
    print(test_model2.model_dump_json())
    # {"id":2,"name":"Bob","age":25}

    print(test_model2.model_json_schema())
    # {'properties': {'id': {'title': 'Id', 'type': 'integer'}, 'name': {'title': 'Name', 'type': 'string'}, 'age': {'title': 'Age', 'type': 'integer'}}, 'required': ['id', 'name', 'age'], 'title': 'TestModel', 'type': 'object'}

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
    
