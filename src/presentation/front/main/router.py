from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from src.presentation.front.templates import templates

main_static = APIRouter()


@main_static.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
