from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn

from src.core.config import config
from src.core.middleware import RequestLoggingMiddleware
from src.core.logger import get_logger

from src.presentation.front import front_router
from src.presentation.api import api_router

from src.utils import create_admin

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(
    _app: FastAPI,
) -> AsyncGenerator[None, None]:  # noqa: ARG001
    base_url: str = f"http://{config.APP_HOST}:{config.APP_PORT}"
    logger.info(f"App started on {base_url}")
    logger.info(f"See Swagger for mode info: {base_url}/docs")
    await create_admin()
    yield
    logger.warning("Stopping app...")


app = FastAPI(title=config.APP_NAME, debug=config.DEBUG, lifespan=lifespan)
app.mount("/static", StaticFiles(directory="src/static"), name="static")

app.add_middleware(RequestLoggingMiddleware)

app.include_router(front_router)
app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(app, host=config.APP_HOST, port=config.APP_PORT, log_level=50)
