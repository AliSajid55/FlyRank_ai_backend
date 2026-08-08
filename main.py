from fastapi import FastAPI
from pydantic import BaseModel
from repository import SQLiteRepository

app = FastAPI()
repo = SQLiteRepository()

class Item(BaseModel):
    title: str
    done: bool = False

@app.get("/")
def root():
    return {"message": "Hello, this is CRUD API"}

@app.get("/health")
def health():
    return {"status": "Everything is working fine!"}

@app.post("/tasks")
def create_item(item: Item):
    saved_item = repo.add(item.dict()) # Repo use karein
    return {"message": "Item added successfully", "item": saved_item}

@app.get("/tasks")
def get_items():
    return {"items": repo.get_all()} # Repo use karein
