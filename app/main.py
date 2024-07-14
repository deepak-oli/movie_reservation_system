import logging
import os 

from fastapi import FastAPI
from app.routers import include_routers

# Disable passlib logging
logging.getLogger('passlib').setLevel(logging.ERROR)

# Initialize logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


app = FastAPI()


@app.get("/")
def read_root():
    return {"status": "Running"}

# add all routers
include_routers(app)



DEBUG_MODE = os.getenv("DEBUG", "false").lower() == "true"

if DEBUG_MODE:
    import debugpy
    debugpy.listen(("0.0.0.0", 5678))
    logger.info("Debug mode enabled")
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)