from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn

from src.core.config import config

from src.presentation.front import front_router

app = FastAPI(title=config.APP_NAME)
app.mount("/static", StaticFiles(directory="src/static"), name="static")

app.include_router(front_router)

if __name__ == "__main__":
    uvicorn.run(app, host=config.APP_HOST, port=config.APP_PORT)
