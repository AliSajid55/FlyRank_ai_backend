from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from repository import SQLiteRepository

app = FastAPI()
repo = SQLiteRepository()

class Item(BaseModel):
    title: str | None = None
    done: bool = False

@app.get("/")
def root():
    return {"message": "Hello, this is CRUD API"}

@app.get("/health")
def health():
    return {"status": "Everything is working fine!"}

@app.post("/tasks")
def create_item(item: Item):
    title = (item.title or "").strip()
    if not title:
        return JSONResponse(status_code=400, content={"error": "Title is required"})
    saved_item = repo.add({"title": title, "done": item.done})
    return JSONResponse(status_code=201, content=saved_item)

@app.get("/tasks")
def get_items():
    return {"items": repo.get_all()} # Repo use karein

@app.get("/tasks/{task_id}")
def get_item(task_id: int):
    item = repo.get_by_id(task_id)
    if item is None:
        return JSONResponse(status_code=404, content={"error": "Task not found"})
    return {"item": item}
