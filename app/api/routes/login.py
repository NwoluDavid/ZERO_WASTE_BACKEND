from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.deps import get_db
from app.models import  Token

from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm

from app.utils import create_access_token
from app import crud

from datetime import timedelta
from app.config import settings

router=APIRouter()

@router.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)]

):
    """"
    The login Auth route , takes the users Email and Password , and returns the user details with the token
    """
    # get user by email
    user = crud.authenticate(
        session=db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(
        access_token=create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        display_name=user.display_name,
        email=user.email,
        phone=user.phone_number,

    )
    
    
#  some code we might need later

    # "User": UserOutput(
    #     display_name=user.display_name,
    #     email=user.email,
    #     phone=user.phone_number,),
        
    # "Token": Token(
    # access_token=create_access_token(
    #     user.id, expires_delta=access_token_expires
    # )