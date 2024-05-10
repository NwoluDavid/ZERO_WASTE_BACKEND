from sqlmodel import SQLModel, Field, Column, VARCHAR ,Relationship ,Enum
from pydantic import EmailStr 

from pydantic_extra_types.phone_numbers import PhoneNumber
from typing import Optional
 
from datetime import date  
from enum import Enum

import uuid



class UserCreate(SQLModel):
    first_name:str = Field(min_length=3, max_length=50, description="Name of the User",  schema_extra={"examples": ["Jonah"]}, title="Name")
    last_name:str = Field(min_length=3, max_length=50, description="Name of the User",  schema_extra={"examples": ["Onah"]}, title="Name")# noqa
    email: EmailStr = Field(sa_column=Column("email", VARCHAR, unique=True, index=True), description="Email of the user",schema_extra={'example': "dave@example.com"})
    phone_number: PhoneNumber = Field(description="Phone number of the user", title="Phone Number" ,schema_extra ={"examples":["+2348103896322"]})  # noqa
    password: str = Field(min_length=8, max_length=100, description="Password of the user",title="Password" , schema_extra={'example': "Dante@123"})  # noqa       

    class Config:
        orm_mode = True
 
 
    
class User(UserCreate, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    waste: list["Waste"] = Relationship(back_populates="user")  
    is_staff: Optional[bool]= Field(default =False)
    is_active:Optional[bool]= Field(default=False)
    review: list["Review"] = Relationship(back_populates="user")
    profile_picture: Optional[str]= Field(default=None)
    
    

    
class UserLogin(SQLModel):
    email: EmailStr = Field(description="Email of the user",)
    password: str = Field(min_length=8, max_length=100, description="Password of the user",title="Password")  # noqa
    
    
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"
    first_name: str
    last_name: str
    email: str
    phone : str


class TokenData(SQLModel):
    sub: uuid.UUID | None =None

class UserOutput(SQLModel):
    id: int = None
    display_name: str
    email: EmailStr
    phone: PhoneNumber
    
class WasteType(str, Enum):
    organic_waste = "Organic"
    plastic_waste ="Plastic"
    medical_waste= "Medical"
    industrial_waste = "Industrial"
    
    
class Amount(int, Enum):
    organic_waste = 1000
    plastic_waste = 2000
    medical_waste = 5000 
    industrial_waste =10000
    
class BookingStatus(str, Enum):
    pending ="PENDING"
    in_transit ="IN TRANSIT"
    delivered ="COMPLETED"   
 
    
class Booking (SQLModel):
    first_name:str = Field(description="user firstname" ,  schema_extra={"examples": ["Jonah"]})
    last_name: str =Field(description="user last name" , schema_extra={"examples": ["Onah"]})
    phone:PhoneNumber =Field(description="the user phonenumber" , schema_extra ={"examples":["+2348103896322"]})
    address: str =Field(description ="User address for pickup",schema_extra={"examples": ["Predia Hotel"]})
    pickup_date:Optional[date]
    waste_type:WasteType = Field(description ="Input the type of waste",schema_extra={"examples": ["Plastic"]})
    user_waste: Optional[str]=None
    amount:Optional[Amount] =Field(default = 1000)
   
    class Config:
        orm_mode = True


# This model is for booking wastes disposal
class Waste(Booking,table=True):
    id:  Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True, index =True)
    user_id: uuid.UUID | None = Field(default_factory=uuid.uuid4, foreign_key="user.id")
    user: User | None = Relationship(back_populates="waste")
    order_status:Optional[BookingStatus] = Field(default = "PENDING")
    delivery_status:Optional[bool]= Field(default=False)
    payment_status: bool = Field(default=False)

    
    

class UserUpdate(SQLModel):
    display_name:str = Field(min_length=3, max_length=50, description="Name of the User", schema_extra={'example': "John Doe"}, title="Name")  # noqa
    email: EmailStr = Field(sa_column=Column("email", VARCHAR, unique=True, index=True), description="Email of the user",schema_extra={'example': "dave@example.com"})
    phone_number: PhoneNumber = Field(description="Phone number of the user", title="Phone Number" ,schema_extra={'example': "+2348103896344"})  # noqa
    password: str = Field(min_length=8, max_length=100, description="Password of the user",title="Password" , schema_extra={'example': "Dante@123"})  # noqa    # noqa
    


class ReviewBase(SQLModel):
    reviewer_name:Optional[str]
    rating: Optional[int]
    comment: str = Field(min_length=4, max_length=300, description="User should give their review")
    
    class Config:
        orm_mode = True

class Review(ReviewBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    user_id: uuid.UUID | None = Field(default_factory=uuid.uuid4, foreign_key="user.id")
    user: User | None = Relationship(back_populates="review")
    

class ForgetPasswordRequest(SQLModel):
    email: str
     

class ResetForgetPassword(SQLModel):
    secret_token:str
    new_password: str


class NewPassword(SQLModel):
    token: str
    new_password: str

class Message(SQLModel):
    message: str
class UpdateDeliveryStatus(SQLModel):
    delivery_status: bool