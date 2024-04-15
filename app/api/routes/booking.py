from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select 
from app.deps import get_db, get_current_user
from app.models import Booking, Waste , User , UserCreate , UserLogin
from typing import Annotated
from sqlalchemy.orm import registry


mapper_registry = registry()

router=APIRouter()

@router.post("/booking" , status_code =201 )
async def booking(waste: Booking,db: Annotated[Session,  Depends(get_db)], user: Annotated[User, Depends(get_current_user)]):
    # if user is not None:
    waste_create = Waste(**waste.dict())
    db.add(waste_create)
    db.commit()
    db.refresh(waste_create)
    return waste_create
  

@router.on_event("startup")
async def startup_event():
    mapper_registry.configure()
    
  
  