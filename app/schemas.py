from pydantic import BaseModel , Field , EmailStr 
from pydantic_extra_types import phone_numbers 
from typing import Optional


class SignUpModel(BaseModel):
    id : Optional[int]=None
    display_name:str = Field(min_length=3, max_length=50, description="Name of the User", schema_extra={'example': "John Doe"}, title="Name")  # noqa
    email: EmailStr = Field(description= "User emails" , examples= "dave@example.com" , title ="Email")
    phone_number: phone_numbers  = Field(description="Phone number of the user", title="Phone Number", examples= "+2348103896344")  # noqa
    password: str = Field(min_length=8, max_length=100, description="Password of the user",title="Password" , examples= "Dante@123") 
    
    class config:
        orm_mode =True
