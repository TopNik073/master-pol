from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from src.presentation.front.templates import templates

admin_static = APIRouter(prefix="/admin")


@admin_static.get("/", response_class=HTMLResponse)
async def admin_index(request: Request):
    return templates.TemplateResponse(
        "admin/index.html",
        {
            "request": request,
        },
    )


@admin_static.get("/users", response_class=HTMLResponse)
async def admin_users(request: Request):
    return templates.TemplateResponse("admin/users.html", {"request": request})


@admin_static.get("/partners", response_class=HTMLResponse)
async def admin_partners(request: Request):
    return templates.TemplateResponse("admin/partners.html", {"request": request})


@admin_static.get("/partners-bids", response_class=HTMLResponse)
async def admin_partners_bids(request: Request):
    return templates.TemplateResponse("admin/partners_bids.html", {"request": request})


@admin_static.get("/products", response_class=HTMLResponse)
async def admin_products(request: Request):
    return templates.TemplateResponse("admin/products.html", {"request": request})


@admin_static.get("/products-import", response_class=HTMLResponse)
async def admin_products_import(request: Request):
    return templates.TemplateResponse(
        "admin/products_import.html", {"request": request}
    )


@admin_static.get("/products-types", response_class=HTMLResponse)
async def admin_products_types(request: Request):
    return templates.TemplateResponse("admin/products_types.html", {"request": request})


@admin_static.get("/materials", response_class=HTMLResponse)
async def admin_materials(request: Request):
    return templates.TemplateResponse("admin/materials.html", {"request": request})
