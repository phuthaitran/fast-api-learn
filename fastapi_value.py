from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def index():
    return {"message": "Hello world"}

@app.get("/items")
async def read_items(q: str | None = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results