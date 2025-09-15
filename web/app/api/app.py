import os
from starlette.requests import Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from api.routers.backend import router as router_backend
from api.routers.frontend import router as router_frontend


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static") # Раздаем статические файлы (например, ваш HTML, CSS, JS)

app.include_router(router_backend)
app.include_router(router_frontend)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)