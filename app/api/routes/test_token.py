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



router =APIRouter()
@router.post("/login/test-token", response_model=UserOutput)
def test_token(current_user: Annotated[User, Depends(get_current_user)]
) -> Any:
    """
    Test access token
    """
    return current_user