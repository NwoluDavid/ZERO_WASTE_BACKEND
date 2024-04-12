from fastapi import FastAPI
from app.api.main import api_router
from sqlmodel import SQLModel
from app.db import engine
from app.config import settings

app = FastAPI(title="ZERO WASTE")
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)
