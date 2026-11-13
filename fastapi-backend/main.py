# main.py
from fastapi import FastAPI

app = FastAPI(title="Career Coach API", description="API for Career Coach Application", version="1.0.0")

@app.get("/")
def read_root():
    return {"message": "Hello World! Your FastAPI backend is running seamlessly."}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
