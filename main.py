from fastapi import FastAPI
from pydantic import BaseModel
from repository import InMemoryRepository # Nai class import karein

app = FastAPI()
repo = InMemoryRepository() # Yahan object bana lein

class Item(BaseModel):
    name: str

@app.get("/")
def root():
    return {"message": "Hello, this is my first API"}

@app.get("/health")
def health():
    return {"status": "Everything is working fine!"}

@app.post("/items")
def create_item(item: Item):
    saved_item = repo.add(item.dict()) # Repo use karein
    return {"message": "Item added successfully", "item": saved_item}

@app.get("/items")
def get_items():
    return {"items": repo.get_all()} # Repo use karein
