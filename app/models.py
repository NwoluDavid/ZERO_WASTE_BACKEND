from sqlmodel import SQLModel, Field, Column, VARCHAR ,Relationship ,Enum
from pydantic import EmailStr 
from pydantic_extra_types.phone_numbers import PhoneNumber
from typing import Optional , List
from datetime import date
from enum import Enum
from sqlalchemy.orm import registry



class UserCreate(SQLModel):
    display_name:str = Field(min_length=3, max_length=50, description="Name of the User", schema_extra={'example': "A very nice Item"}, title="Name")  # noqa
    email: EmailStr = Field(sa_column=Column("email", VARCHAR, unique=True, index=True), description="Email of the passenger",)
    phone_number: PhoneNumber = Field(description="Phone number of the passenger", title="Phone Number")  # noqa
    password: str = Field(min_length=8, max_length=100, description="Password of the passenger",title="Password")  # noqa        
    class Config:
        orm_mode = True
class User(UserCreate, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    waste: list["Waste"] = Relationship(back_populates="user")
    
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
    
class WasteType(str, Enum):
    house_hold = "house hold waste"
    industrial ="Industrial waste"
    Organizational = "Organizational waste"
    
class Amount(int, Enum):
    house_hold= 1000
    industrial = 10000
    organizational = 50000    
    
class Booking (SQLModel):
    first_name:str
    last_name: str
    phone:PhoneNumber
    address: str
    pickup_date: date
    waste_type:WasteType 
    user_waste: Optional[str]=None
    amount: Amount
    # user_id: int | None = Field(default=None, foreign_key="user.id")
    class Config:
        orm_mode = True

class Waste(Booking,table=True):
    id:  Optional[int] = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="user.id")
    # user: list["User"] = Relationship(back_populates="WasteModel")
    user: User | None = Relationship(back_populates="waste")
    
    
    # training_status: TrainingStatus = Field(sa_column=Column(Enum(TrainingStatus)))
        
    

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
    id: Optional [int] = Field(default=None, primary_key=True)

class ForgetPasswordRequest(SQLModel):
    email: str
     


