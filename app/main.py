import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status
from sqlalchemy import text


from app.routers import auth, user

from app.config.redis import get_redis_client
from app.dependencies import get_db


# Disable passlib logging
logging.getLogger('passlib').setLevel(logging.ERROR)

# Initialize logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # check if the Redis server is running
    try:
        _ = get_redis_client()
        logger.info("Successfully connected to Redis.")
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Internal Server Error: Unable to connect to Redis."
        )
    
    # check if the database connection is working
    db = next(get_db())
    try:
        db.execute(text("SELECT 1"))
        logger.info("Successfully connected to the database.")

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Internal Server Error: Unable to connect to the database."
        )
    finally:
        db.close()
    yield
    # Clean up code here

app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"status": "Running"}

app.include_router(auth.router)
app.include_router(user.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)