from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

item_list = []

app = FastAPI()

@app.get("/")
def index():
    return {"message": "Hello world"}

@app.post("/items")
async def create_item(item: Item):
    item_list.append(item)
    return item

@app.get("/list-items")
async def list_item(limit: int = 10):
    return item_list[0:limit]

@app.get("/list-items/{item_id}")
def list_iteam(item_id: int):
    return item_list[item_id]