
from datetime import datetime, timedelta
from typing import Any

from app.config import settings
from jose import jwt, JWTError

from passlib.context import CryptContext
from app.models import TokenData

from pydantic import ValidationError
from fastapi import HTTPException, status, Depends

from dataclasses import dataclass
from jinja2 import Template

from pathlib import Path
import emails
 
import smtplib, ssl
from email.message import EmailMessage





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

    
def send_email(emai_to:str, subject:str , html_content:str):
    
    port = 587
    smtp_server = "smtp.zeptomail.com"
    username="emailapikey"
    password = "wSsVR61+rxPyB60uzmD+dr86mQtRDg7xFkV82Vvw73H6Fq3H9sczkRecDQ7zFPQfE2JrRjsUrLkhmkgH2jFbit0rz1hWCyiF9mqRe1U4J3x17qnvhDzDV2pUkRWML4IKwQVqnWRlGs8h+g=="
    message = "Test email sent successfully."
    msg = EmailMessage()
    msg['Subject'] = "Test Email"
    msg['From'] = "noreply@zerowastebin.com.ng"
    msg['To'] = "nwoludave@gmail.com"
    msg.set_content(message)
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