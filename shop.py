from enum import Enum
from typing import Any, Annotated

from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel

app = FastAPI(
    title="Tony's shop",
    description="Cheapest tools and consumables in Hanoi",
    version="0.1.0"
)

class Category(Enum):
    """Category of an item"""
    
    TOOLS = "tools"
    CONSUMABLES = "consumables"
    
class Item(BaseModel):
    name: str
    price: float
    count: int
    id: int
    category: Category
    description: str | None = None
    
items = {
    0: Item(name="Hammer", price=9.99, count=20, id=0, category=Category.TOOLS, description="The strongest hammer you can have for $10"),
    1: Item(name="Pliers", price=5.99, count=20, id=1, category=Category.TOOLS),
    2: Item(name="Nails", price=1.99, count=100, id=2, category=Category.CONSUMABLES)
}

@app.get("/")
def index() -> dict[str, dict[int, Item]]:
    return {"items": items}

# Path: get items by id
@app.get("/items/{item_id}")
def query_items_by_id(item_id: int) -> Item:
    if item_id not in items:
        raise HTTPException(status_code=404, detail=f"Item with {item_id} does not exist")
    return items[item_id]

@app.get("/items/")
def query_items_by_parameters(
    name: str | None = None,
    price: float | None = None,
    count: Annotated[int | None, Query(description="Returns item with equal or larger than the given number")] = None,
    category: Category | None = None
) -> dict[str, Any]:
    def check_item(item: Item) -> bool:
        return all(
            (
                name is None or item.name == name,
                price is None or item.price == price,
                count is None or item.count >= count,
                category is None or item.category is category                
            )
        )
        
    selection = [item for item in items.values() if check_item(item)]
    
    return {
        "query": {"name": name, "price": price, "count": count, "category": category},
        "selection": selection
    }

# Add an item    
@app.post("/")
def add_item(item: Item) -> dict[str, Item]:
    if item.id in items:
        raise HTTPException(status_code=400, detail=f"Item with {item.id} already exists.")
        
    items[item.id] = item
    return {"added": item}

# Update an item
@app.put("/items/{item_id}")
def update(
    item_id: int = Path(ge=0),
    name: Annotated[str | None, Query(min_length=1, max_length=20)] = None,
    price: Annotated[float | None, Query(gt=0.0)] = None,
    count: Annotated[int | None, Query(ge=0)] = None,
    description: str|None = None
) -> dict[str, Item]:
    if item_id not in items:
        raise HTTPException(status_code=404, detail=f"Item with {item_id} does not exist")
    if all(info is None for info in (name, price, count, description)):
        raise HTTPException(status_code=400, detail="No parameters provided for update")
    
    item = items[item_id]
    if name is not None:
        item.name = name
    if price is not None:
        item.price = price
    if count is not None:
        item.count = count
    if description is not None:
        item.description = description
        
    return {"updated": item}

# Delete an item
@app.delete("/items/{item_id}")
def delete_item(item_id: int) -> dict[str, Item]:
    if item_id not in items:
        raise HTTPException(status_code=404, detail=f"Item with {item_id} does not exist")
    item = items.pop(item_id)
    return {"deleted": item}