from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select
from app.deps import get_db, get_current_user
from app.models import UserCreate, User, UserLogin, Token, UserOutput,UserUpdate
from typing import Annotated, Any
from fastapi.security import OAuth2PasswordRequestForm
from app.utils import get_password_hash, verify_password, create_access_token
from datetime import timedelta
from app.config import settings
from app.crud import update_user, get_user_by_id, delete_user
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import registry


mapper_registry = registry()

router = APIRouter()

@router.post("/register")
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


@router.on_event("startup")
async def startup_event():
    mapper_registry.configure()

@router.get("/profile/{user_id}")
def get_user_profile(user_id: int, current_user: int = Depends(get_current_user), db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if not user:   
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.patch("/profile/{user_id}")
def update_user_profile_patch(user_id: int, user_data: UserUpdate, current_user: int = Depends(get_current_user), db: Session = Depends(get_db)):
    updated_user = update_user(db, user_id, user_data)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.put("/profile/{user_id}")
def update_user_profile(user_id: int, user_data: UserUpdate, current_user: int = Depends(get_current_user), db: Session = Depends(get_db)):
    updated_user = update_user(db, user_id, user_data)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/profile/{user_id}")
def delete_user_profile(user_id: int, current_user: int = Depends(get_current_user), db: Session = Depends(get_db)):
    deleted_user = delete_user(db, user_id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}