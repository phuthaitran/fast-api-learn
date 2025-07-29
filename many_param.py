from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class User(BaseModel):
    username: str
    full_name: str | None = None

items = {
    0: [Item(name="foo", description="the pretender", price=36, tax=1),User(username="tony", full_name="Tony Tran")]
}

@app.get("/items")
def list_items():
    return items

@app.post("/items/{item_id}")
async def update_item(item_id: int, item: Item, user: User):
    if item_id in items:
        raise HTTPException(status_code=400, detail=f"Item with {item.id} already exists.")
    
    result = {"item": item, "user": user}
        
    items[item.id] = result
    return {"added": result}