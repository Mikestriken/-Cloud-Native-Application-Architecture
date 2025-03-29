from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str
    price: float
    
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id, "message": "Item retrieved successfully"}

@app.post("/items/")
def create_item(item: Item):
    return {"message": "Item created successfully", "item": item}