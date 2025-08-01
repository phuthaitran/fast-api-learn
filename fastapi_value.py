from typing import Annotated

from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/")
def index():
    return {"message": "Hello world"}

@app.get("/items")
async def read_items(q: Annotated[str | None, Query(max_length=10)] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results