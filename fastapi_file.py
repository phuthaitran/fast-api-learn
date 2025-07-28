from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def index():
    return {"message": "Hello world"}

fake_items_db = [
    {"item_name": "Foo"},
    {"item_name": "Bar"},
    {"item_name": "Baz"},
    {"item_name": "Cat"},
    {"item_name": "Dog"},
    {"item_name": "Cow"},
    {"item_name": "Joy"},
    {"item_name": "Bee"},
    {"item_name": "Rat"},
    {"item_name": "Jog"},
    {"item_name": "Bog"},
    {"item_name": "Boo"}
]

@app.get("/items")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item