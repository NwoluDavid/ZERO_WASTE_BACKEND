
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
import emails 
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

def send_email(email_to: str, subject: str, html_content: str):
    message = emails.Message(
        subject=subject, html=html_content, mail_from=settings.EMAILS_FROM_NAME
    )
    smtp_options = {
        "host": settings.SMTP_HOST,
        "port": settings.SMTP_PORT,
        "user": settings.SMTP_USER,
        "password": settings.SMTP_PASSWORD,
    }
    if settings.SMTP_TLS:
        smtp_options["tls"] = True
    elif settings.SMTP_SSL:
        smtp_options["ssl"] = True
    response = message.send(to=email_to, smtp=smtp_options)




def create_reset_password_token(email:str):
    data={"sub":email , "exp":datetime.utcnow() + timedelta(minutes =10)}
    token = jwt.encode(data , settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token


# def save_profile_picture(profile_picture: UploadFile, user_id: int):
#     # Validate picture type
#     allowed_types = ["jpeg", "png", "jpg"]
#     file_extension = profile_picture.filename.split(".")[-1]
#     if file_extension.lower() not in allowed_types:
#         raise HTTPException(status_code=400, detail="Unsupported picture format")

#     # Create directory if it doesn't exist
#     directory = os.path.join("profile_pictures", str(user_id))
#     os.makedirs(directory, exist_ok=True)

#     # Save the profile picture to the file directory
#     file_path = os.path.join(directory, profile_picture.filename)
#     with open(file_path, "wb") as f:
#         f.write(profile_picture.file.read())

#     # Validate and resize the image
#     with Image.open(file_path) as img:
#         img.verify()  # Verify image integrity
#         img.thumbnail((300, 300))  # Resize image to max size (300x300)
#         img.save(file_path)  # Save the resized image

#     return file_path

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
    
