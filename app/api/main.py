from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select
from app.deps import get_db, get_current_user
from app.models import UserCreate, User, UserLogin, Token, UserOutput
from typing import Annotated, Any
from fastapi.security import OAuth2PasswordRequestForm
from app.utils import get_password_hash, verify_password, create_access_token
import app.crud
from datetime import timedelta
from app.config import settings
from fastapi import APIRouter
from .routes import items, login, users, test_token, reviews ,booking
from sqlalchemy.orm import registry



# Define your models and relationships


api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(items.router, prefix="/items", tags=["Items"])
api_router.include_router(reviews.router, prefix="/reviews", tags=["Reviews"])
api_router.include_router(login.router, tags=["users"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(booking.router, prefix="/bad", tags=["Waste"])
api_router.include_router(test_token.router, prefix="/utils", tags=["utils"])

