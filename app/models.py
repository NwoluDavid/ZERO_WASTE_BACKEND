from sqlmodel import SQLModel, Field, Column, VARCHAR
from pydantic import EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber
from typing import Optional
import datetime


class UserCreate(SQLModel):
    display_name:str = Field(min_length=3, max_length=50, description="Name of the User", schema_extra={'example': "A very nice Item"}, title="Name")  # noqa
    email: EmailStr = Field(sa_column=Column("email", VARCHAR, unique=True, index=True), description="Email of the passenger",)
    phone_number: PhoneNumber = Field(description="Phone number of the passenger", title="Phone Number")  # noqa
    password: str = Field(min_length=8, max_length=100, description="Password of the passenger",title="Password")  # noqa        

class User(UserCreate, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
class UserLogin(SQLModel):
    email: EmailStr = Field(description="Email of the passenger",)
    password: str = Field(min_length=8, max_length=100, description="Password of the passenger",title="Password")  # noqa
    
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(SQLModel):
    sub: int | None = None

class UserOutput(SQLModel):
    id: int
    display_name: str
    email: EmailStr
    phone: PhoneNumber

class UserUpdate(SQLModel):
    display_name:str = Field(min_length=3, max_length=50, description="Name of the User", schema_extra={'example': "A very nice Item"}, title="Name")  # noqa
    email: EmailStr = Field(sa_column=Column("email", VARCHAR, unique=True, index=True), description="Email of the passenger",)
    phone_number: PhoneNumber = Field(description="Phone number of the passenger", title="Phone Number")  # noqa
    password: str = Field(min_length=8, max_length=100, description="Password of the passenger",title="Password")  # noqa


class ReviewBase(SQLModel):
    reviewer_name: str
    rating: int
    comment: str

class Review(ReviewBase, table=True):
    id: int = Field(default=None, primary_key=True)
     


