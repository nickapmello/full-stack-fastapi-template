from fastapi import APIRouter, HTTPException, status
from typing import List
from pydantic import BaseModel

class InventoryItem(BaseModel):
    id: int
    name: str
    description: str
    price: float
    stock: int

# Banco de dados simulado
fake_inventory_db = []

inventory_router = APIRouter()

@inventory_router.get("/", response_model=List[InventoryItem])
def get_items():
    return fake_inventory_db

@inventory_router.get("/{item_id}", response_model=InventoryItem)
def get_item(item_id: int):
    item = next((item for item in fake_inventory_db if item["id"] == item_id), None)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@inventory_router.post("/", response_model=InventoryItem, status_code=status.HTTP_201_CREATED)
def add_item(item: InventoryItem):
    item_dict = item.dict()
    item_dict['id'] = len(fake_inventory_db) + 1
    fake_inventory_db.append(item_dict)
    return item_dict

@inventory_router.put("/{item_id}", response_model=InventoryItem)
def update_item(item_id: int, item: InventoryItem):
    index = next((index for index, p in enumerate(fake_inventory_db) if p["id"] == item_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Item not found")
    fake_inventory_db[index] = item.dict()
    return item.dict()

@inventory_router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_item(item_id: int):
    global fake_inventory_db
    item_index = next((index for index, item in enumerate(fake_inventory_db) if item["id"] == item_id), None)
    if item_index is None:
        raise HTTPException(status_code=404, detail="Item not found")
    del fake_inventory_db[item_index]
    return None
