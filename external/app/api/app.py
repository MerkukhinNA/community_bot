from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from api.routers.frontend import router as router_frontend
from api.routers.backend.user import router as router_user
from api.routers.backend.event import router as router_event
from api.routers.backend.visit import router as router_visit
from api.routers.backend.feedback import router as router_feedback
from api.routers.backend.community import router as router_community


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")  # Раздача статических файлов

app.include_router(router_user)
app.include_router(router_visit)
app.include_router(router_event)
app.include_router(router_feedback)
app.include_router(router_frontend)
app.include_router(router_community)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)