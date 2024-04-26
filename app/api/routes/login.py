from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.deps import get_db
from app.models import  Token , User

from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm

from app.utils import create_access_token
from app import crud

from datetime import timedelta
from app.config import settings

from app.crud import get_user_by_email
from app.crud import get_user_by_email

from app.utils import create_token,send_email , generate_verification_email
from fastapi.responses import JSONResponse


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
        first_name=user.first_name,
        last_name = user.last_name,
        email=user.email,
        phone=user.phone_number,

    )
    

@router.post("/login/{email}")
async def login_verify_email(email:str , db: Annotated[Session, Depends(get_db)]):
    user = db.query(User).filter(User.email == email).first()
    
    """"This route allows the user to still verify his email , when logged in.
    note a user is still allowed to login when he/she registers.
    """
    if user is None:
            return  HTTPException(status_code = status.HTTP_400_BAD_REQUEST, 
            detail="User is not registered"
        )
        
    if user.is_active:
        return  HTTPException(status_code = status.HTTP_400_BAD_REQUEST, 
            detail="User already Verified"
        )
    
    token = create_token(subject=user.email, type_ops="verify")
    data = generate_verification_email(email_to=user.email, email= user.email , token=token)
    send_email(email_to=user.email ,subject =data.subject, html_content = data.html_content)       
    
    return JSONResponse(status_code =200, content={ "message": "A mail to verify your Email have been sent "})        
            
        
    
