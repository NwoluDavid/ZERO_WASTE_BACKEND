from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.main import api_router
from sqlmodel import SQLModel

from app.db import engine
from app.config import settings

from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import registry

from fastapi.staticfiles import StaticFiles
from app.api.general_pages.route_homepage import general_pages_router

def include_router(app):
    app.include_router(general_pages_router)

def start_application():
    app = FastAPI(title="ZERO WASTE")
    app.include_router(api_router, prefix=settings.API_V1_STR)
    include_router(app)
    return app
 
app = start_application()    
    
mapper_registry = registry()

app.add_middleware(
    CORSMiddleware,
    allow_origins =["*"],
    allow_credentials =True,
    allow_methods=["*"],
   allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)
    mapper_registry.configure()

app.mount("/profile_pictures", StaticFiles(directory="profile_pictures"), name="profile_pictures")
