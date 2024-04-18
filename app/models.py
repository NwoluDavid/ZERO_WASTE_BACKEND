from sqlmodel import SQLModel, Field, Column, VARCHAR ,Relationship ,Enum
from pydantic import EmailStr 
from pydantic_extra_types.phone_numbers import PhoneNumber
from typing import Optional , List
from datetime import date
from enum import Enum
from sqlalchemy.orm import registry
import uuid



class UserCreate(SQLModel):
    display_name:str = Field(min_length=3, max_length=50, description="Name of the User", schema_extra={'example': "John Doe"}, title="Name")  # noqa
    email: EmailStr = Field(sa_column=Column("email", VARCHAR, unique=True, index=True), description="Email of the user",schema_extra={'example': "dave@example.com"})
    phone_number: PhoneNumber = Field(description="Phone number of the user", title="Phone Number" ,schema_extra={'example': "+2348103896344"})  # noqa
    password: str = Field(min_length=8, max_length=100, description="Password of the user",title="Password" , schema_extra={'example': "Dante@123"})  # noqa       
    class Config:
        orm_mode = True
 
 
    
class User(UserCreate, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    waste: list["Waste"] = Relationship(back_populates="user")

    
class UserLogin(SQLModel):
    email: EmailStr = Field(description="Email of the user",)
    password: str = Field(min_length=8, max_length=100, description="Password of the user",title="Password")  # noqa
    
    
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"
    display_name: str
    email: str
    phone : str


class TokenData(SQLModel):
    sub: uuid.UUID | None = None

class UserOutput(SQLModel):
    id: int = None
    display_name: str
    email: EmailStr
    phone: PhoneNumber
    
class WasteType(str, Enum):
    organic_waste = "Organic waste"
    plastic_waste ="Industrial waste"
    medical_waste = "Medical waste"
    industrial_waste = "Industrial waste"
    
    
class Amount(int, Enum):
    organic_waste = 1000
    plastic_waste = 2000
    medical_waste = 5000 
    industrial_waste =10000
    
class BookingStatus(str, Enum):
    pending ="PENDING"
    in_transit ="IN TRANSIT"
    delivered ="DELIVERED"   
    
class Booking (SQLModel):
    first_name:str
    last_name: str
    phone:PhoneNumber
    address: str
    pickup_date: date
    waste_type:WasteType 
    user_waste: Optional[str]=None
    amount: Amount
    order_status: BookingStatus
   
    class Config:
        orm_mode = True


# This model is for booking wastes disposal
class Waste(Booking,table=True):
    id:  Optional[uuid.UUID ] = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID | None = Field(default_factory=uuid.uuid4, foreign_key="user.id")
    user: User | None = Relationship(back_populates="waste")
    

class UserUpdate(SQLModel):
    display_name:str = Field(min_length=3, max_length=50, description="Name of the User", schema_extra={'example': "John Doe"}, title="Name")  # noqa
    email: EmailStr = Field(sa_column=Column("email", VARCHAR, unique=True, index=True), description="Email of the user",schema_extra={'example': "dave@example.com"})
    phone_number: PhoneNumber = Field(description="Phone number of the user", title="Phone Number" ,schema_extra={'example': "+2348103896344"})  # noqa
    password: str = Field(min_length=8, max_length=100, description="Password of the user",title="Password" , schema_extra={'example': "Dante@123"})  # noqa    # noqa


class ReviewBase(SQLModel):
    reviewer_name: str
    rating: int
    comment: str

class Review(ReviewBase, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    user_id: uuid.UUID|None = Field(default=None, foreign_key="user.id")

class ForgetPasswordRequest(SQLModel):
    email: str
     


