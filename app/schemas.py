from pydantic import BaseModel , Field , EmailStr 
from pydantic_extra_types.phone_numbers import PhoneNumber
from typing import Optional


class SignUpModel(BaseModel):
    display_name:str = Field(min_length=3, max_length=50, description="Name of the User", title="Name")  # noqa
    email: EmailStr = Field(description= "User emails" , examples= "dave@example.com" , title ="Email")
    phone_number: PhoneNumber = Field(description="Phone number of the user", title="Phone Number", examples= "+2348103896344")  # noqa
    password: str = Field(min_length=8, max_length=100, description="Password of the user",title="Password" , examples= "Dante@123") 
    
    class config:
        orm_mode =True
        schema_extra={
            "example": {
                "display_name": "John",
                "email": "dave@gmail.com",
                "phone_number": "+2348103896344",
                "password": "PASSWORD"
            }
        }
        
class ConnectionConfig(BaseModel):
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: str
    MAIL_SERVER: str
    MAIL_FROM_NAME: str = ""
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = False
    VALIDATE_CERTS: bool = True


        