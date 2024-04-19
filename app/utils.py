
from datetime import datetime, timedelta
from typing import Any
from app.config import settings
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.models import TokenData
from pydantic import ValidationError
from fastapi import HTTPException, status, Depends




pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def create_access_token(subject: str | Any, expires_delta: timedelta) -> str: #subject what we want to encode, expires_delta when the token will expire
    expire = datetime.utcnow() + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_token_access(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        token_data = TokenData(**payload)
    except (JWTError, ValidationError) as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    return token_data

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_reset_password_token(email:str):
    data={"sub":email , "exp":datetime.utcnow() + timedelta(minutes =10)}
    token = jwt.encode(data , settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token
   
def decode_reset_password_token(token:str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        email:str = payload.get("sub") 
        return email
    except JWTError:
        return None 
    

# def generate_reset_password_email(email_to:str, email:str, token:str)->EmailData:
#     project_name = settings.ZEROWASTE  