from typing import Union
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# To run app from terminal => 'uvicorn main:app'
app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

# In place of a database, a dictionary is used
items_database = {}
item_id_counter = 1

@app.get("/")
def read_root():
    return {"Welcome to": "FastAPI"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    if item_id not in items_database:
        raise HTTPException(status_code=404, detail="Item not found")

    item = items_database[item_id]
    response = {
        "item_id": item_id,
        "name": item.name,
        "price": item.price,
        "is_offer": item.is_offer,
        "q": q
    }
    
    return response

@app.post("/items/")
def create_item(item: Item):
    global item_id_counter

    new_item_id = item_id_counter
    items_database[new_item_id] = item
    item_id_counter += 1
    
    return {"item_id": new_item_id, "message": "Item created successfully"}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    if item_id not in items_database:
        raise HTTPException(status_code=404, detail="Item not found")
    
    items_database[item_id] = item
    
    return {"item_id": item_id, "message": "Item updated successfully"}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in items_database:
        raise HTTPException(status_code=404, detail="Item not found")
    
    del items_database[item_id]
    
    return {"item_id": item_id, "message": "Item deleted successfully"}
