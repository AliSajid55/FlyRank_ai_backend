from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello, this is my first API for FlyRank.ai"}

@app.get("/health")
def health():
    return {"status": "Everything is working fine!"}

