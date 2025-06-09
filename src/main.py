from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn

from src.presentation.front import front_router

app = FastAPI()
app.mount("/static", StaticFiles(directory="src/static"), name="static")

app.include_router(front_router)

if __name__ == "__main__":
    uvicorn.run(app)
