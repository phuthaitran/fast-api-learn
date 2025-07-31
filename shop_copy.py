from enum import Enum
from typing import Any, Annotated

from fastapi import FastAPI, HTTPException, Path, Query, Body
from pydantic import BaseModel

app = FastAPI(
    title="Tony's shop",
    description="Cheapest tools and consumables in Hanoi",
    version="0.1.0"
)

# class Category(Enum):
#     """Category of an item"""
    
#     TOOLS = "tools"
#     CONSUMABLES = "consumables"
    
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    
class User(BaseModel):
    username: str
    full_name: str | None = None
    
# items = {
#     0: Item(name="Hammer", price=9.99, count=20, id=0, category=Category.TOOLS, description="The strongest hammer you can have for $10"),
#     1: Item(name="Pliers", price=5.99, count=20, id=1, category=Category.TOOLS),
#     2: Item(name="Nails", price=1.99, count=100, id=2, category=Category.CONSUMABLES)
# }

items = [
    {
        "item_id": 1,
        "item": Item(name="Hammer", description=None, price=8.5, tax=0),
        "user": User(username="tony", full_name="Tony Tran"),
        "importance": 1
    }
]

@app.get("/")
def index():
    return {"items": items}


@app.post("/")
async def add_item(
    item_id: int,
    item: Item,
    user: User,
    importance: int = Body(..., gt=0),
    q: str | None = None
):
    # Check if an item with this ID already exists
    for existing_item in items:
        if existing_item["item_id"] == item_id:
            raise HTTPException(status_code=400, detail=f"Item with ID {item_id} already exists.")
    
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    if user: 
        results.update({"user": user})
    if importance:
        results.update({"importance": importance})
    items.append(results)
    return results
    
    

# Update parameters
@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int = Path(...,title="The ID of the item to get", ge=0, le=150),
    q: str | None = None,
    item: Item | None = None,
    user: User | None = None,
    importance: Annotated[int | None, Body(...,gt=0)] = None
):
    # Find the item with matching item_id
    result = None
    for item_ in items:
        if item_["item_id"] == item_id:
            result = item_
            break
    
    if result is None:
        raise HTTPException(status_code=404, detail=f"Item with {item_id} does not exist")
    
    # Update the fields if provided
    if q is not None:
        result["q"] = q
    if item is not None:
        result["item"] = item
    if user is not None:
        result["user"] = user
    if importance is not None:
        result["importance"] = importance
        
    return {"updated": result}
    
# Path: get items by id
@app.get("/items/{item_id}")
def query_items_by_id(item_id: int):
    for item in items:
        if item["item_id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail=f"Item with {item_id} does not exist")

@app.get("/items/")
def query_items_by_name(name: str | None = None):
    if name is None:
        return {"items": items}
    
    matched_items = []
    for item in items:
        # Check if the item has 'item' key and if that item has a name that matches
        if "item" in item and isinstance(item["item"], Item) and item["item"].name.lower() == name.lower():
            matched_items.append(item)
    
    if not matched_items:
        raise HTTPException(status_code=404, detail=f"No items found with name: {name}")
    
    return {"items": matched_items}

@app.get("/items-by-importance")
def query_items_by_importance(importance: int):
    matched_items = []
    for item in items:
        if item["importance"] == importance:
            matched_items.append(item)
            
    if not matched_items:
        raise HTTPException(status_code=404, detail=f"No items found with importance of {importance}")
    
    return {"items": matched_items}