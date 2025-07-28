from fastapi import FastAPI, HTTPException

app = FastAPI()

items = []

# Define root path
@app.get("/")
def index():
    return {"name": "Hello world"}

# Create a new item
@app.post("/items")
def create_item(item: str):
    items.append(item)
    return items

# List items
@app.get("/items")
def list_items(limit: int = 10):
    return items[0:limit]

# Get item by its ID
@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id < len(items):
        return items[item_id]
    else:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found ")