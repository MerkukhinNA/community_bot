import os
from fastapi import APIRouter
from starlette.requests import Request
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/favicon.ico")
async def favicon():
    return FileResponse(os.path.join('static', 'favicon.ico'))

@router.get("/", tags=['root']) 
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/auth", tags=['root']) 
async def read_root(request: Request):
    return templates.TemplateResponse("auth.html", {"request": request})

@router.get("/main-menu", tags=['root']) 
async def read_root(request: Request):
    return templates.TemplateResponse("main-menu.html", {"request": request})

@router.get("/event/reserve", tags=['root']) 
async def read_root(request: Request):
    return templates.TemplateResponse("event/reserve.html", {"request": request})

@router.get("/event/my", tags=['root']) 
async def read_root(request: Request):
    return templates.TemplateResponse("event/my.html", {"request": request})

@router.get("/admin/menu", tags=['root']) 
async def read_root(request: Request):
    return templates.TemplateResponse("admin/menu.html", {"request": request})

@router.get("/admin/feedback", tags=['root']) 
async def read_root(request: Request):
    return templates.TemplateResponse("admin/feedback.html", {"request": request})

@router.get("/admin/community/create", tags=['root']) 
async def read_root(request: Request):
    return templates.TemplateResponse("admin/community-create.html", {"request": request})

@router.get("/admin/community/delete", tags=['root']) 
async def read_root(request: Request):
    return templates.TemplateResponse("admin/community-delete.html", {"request": request})

@router.get("/admin/community/update", tags=['root']) 
async def read_root(request: Request):
    return templates.TemplateResponse("admin/community-update.html", {"request": request})

@router.get("/admin/event/create", tags=['root']) 
async def read_root(request: Request):
    return templates.TemplateResponse("admin/event-create.html", {"request": request})

@router.get("/admin/event/delete", tags=['root']) 
async def read_root(request: Request):
    return templates.TemplateResponse("admin/event-delete.html", {"request": request})

@router.get("/admin/visit/delete", tags=['root']) 
async def read_root(request: Request):
    return templates.TemplateResponse("admin/visit-delete.html", {"request": request})

@router.get("/feedback/menu", tags=['root']) 
async def read_root(request: Request):
    return templates.TemplateResponse("feedback/menu.html", {"request": request})

@router.get("/feedback/create", tags=['root']) 
async def read_root(request: Request):
    return templates.TemplateResponse("feedback/create.html", {"request": request})

@router.get("/feedback/my", tags=['root']) 
async def read_root(request: Request):
    return templates.TemplateResponse("feedback/my.html", {"request": request})