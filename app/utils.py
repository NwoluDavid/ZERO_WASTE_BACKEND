from datetime import datetime, timedelta
from typing import Any

from app.config import settings
from jose import jwt, JWTError

from passlib.context import CryptContext
from app.models import TokenData

from pydantic import ValidationError
from fastapi import HTTPException, status, Depends, UploadFile
from dataclasses import dataclass
from jinja2 import Template

from pathlib import Path
 
import smtplib, ssl
from email.message import EmailMessage

import requests
import os

import uuid
from PIL import Image



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@dataclass
class EmailData:
    html_content: str
    subject: str



def create_access_token(subject: str | Any, expires_delta: timedelta) -> str: #subject what we want to encode, expires_delta when the token will expire
    expire = datetime.utcnow() + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def create_token(subject: str | Any, type_ops: str):
    if type_ops == "verify":
        hours = settings.EMAIL_VERIFY_EMAIL_EXPIRE_MINUTES
    elif type_ops == "reset":
        hours = settings.EMAIL_RESET_PASSWORD_EXPIRE_MINUTES
    elif type_ops == "access":
        hours = settings.ACCESS_TOKEN_EXPIRE_MINUTES

    expire = datetime.utcnow() + timedelta(
        hours=hours
    )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
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

def verify_token(token: str) -> str | None:
    try:
        decoded_token = jwt.decode(
            token, settings.SECRET_KEY, algorithms=settings.ALGORITHM
        )  # noqa
        print(decoded_token, "decoded_token")
        return str(decoded_token["sub"])
    except JWTError:
        return None
def render_email_template(*, template_name: str, context: dict[str, Any]) -> str:
    template_str = (
        Path(__file__).parent / "email-templates" / template_name
    ).read_text()
    html_content = Template(template_str).render(context)
    return html_content

def generate_verification_email(email_to: str, email: str, token: str):
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Email verification for user {email}"
    link = f"{settings.FRONTEND_URL}verify-email?token={token}"

    html_content = render_email_template(
        template_name="verify_email.html",
        context={
            "project_name": settings.PROJECT_NAME,
            "username": email,
            "email": email_to,
            "valid_hours": settings.EMAIL_VERIFY_EMAIL_EXPIRE_MINUTES,
            "link": link,
        },
    )
    return EmailData(html_content=html_content, subject=subject)


def generate_reset_password_email(email_to: str, email: str, token: str):
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Password recovery for user {email}"
    link = f"{settings.FRONTEND_URL}reset-password?token={token}"

    html_content = render_email_template(
        template_name="reset_password.html",
        context={
            "project_name": settings.PROJECT_NAME,
            "username": email,
            "email": email_to,
            "valid_hours": settings.EMAIL_RESET_PASSWORD_EXPIRE_MINUTES,
            "link": link,
        },
    )
    return EmailData(html_content=html_content, subject=subject)


def create_reset_password_token(email:str):
    data={"sub":email , "exp":datetime.utcnow() + timedelta(minutes =10)}
    token = jwt.encode(data , settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token


def get_image_url(image_filename: str):
    return f"/profile_pictures/{image_filename}"

def validate_picture(picture: UploadFile):
    if not picture.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        raise HTTPException(status_code=400, detail="Please upload a picture in JPEG, JPG or PNG format.")

def save_profile_picture(picture: UploadFile):
    contents = picture.file.read()
    if len(contents) > 10 * 1024 * 1024:  # 10 MB limit
        raise HTTPException(status_code=400, detail="File size exceeds limit (10MB).")

    file_extension = picture.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    upload_folder = "./profile_pictures"
    file_path = os.path.join(upload_folder, unique_filename)

    os.makedirs(upload_folder, exist_ok=True)
    with open(file_path, "wb") as file_object:
        file_object.write(contents)
    
    return file_path 
    

    
def send_email(email_to:str, subject:str , html_content:str):
    
    port =  587
    smtp_server = settings.SMTP_HOST
    username=settings.SMTP_USER
    password = settings.SMTP_PASSWORD
    message = html_content
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = "noreply@zerowastebin.com.ng"
    msg['To'] = email_to
    msg.add_alternative(message, subtype="html")
    try:
        if port == 465:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(username, password)
                server.send_message(msg)
        elif port == 587:
            with smtplib.SMTP(smtp_server, port) as server:
                server.starttls()
                server.login(username, password)
                server.send_message(msg)
        else:
            print ("use 465 / 587 as port value")
            exit()
        print ("successfully sent")
    except Exception as e:
        print (e)
        
        
def verify_payment(ref_id:str):
    paystack_url = settings.PAYMENT_URL
    url_path = paystack_url + f"transaction/verify/{ref_id}"
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json",
    }
    response = requests.get(url_path, headers=headers)
    
    if response.status_code == 200:
        response_data = response.json()
        return response_data['status'], response_data['data']
    
    response_data = response.json()
    return response_data['status'], response_data['data'] 
