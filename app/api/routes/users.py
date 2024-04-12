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

router = APIRouter()

@router.post("/register", tags=["login"])
async def register(
    user: UserCreate, 
    db: Annotated[Session,  Depends(get_db)]
):
    #hash the password
    user.password = get_password_hash(user.password)
    new_user = User( 
        display_name= user.display_name,       
        email=user.email,
        email_verified=False,
        phone_number=user.phone_number.split(":")[1],
        password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return user