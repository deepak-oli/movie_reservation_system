import logging
from fastapi import FastAPI
from app.routers import auth

# Disable passlib logging
logging.getLogger('passlib').setLevel(logging.ERROR)

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "Running"}

app.include_router(auth.router)