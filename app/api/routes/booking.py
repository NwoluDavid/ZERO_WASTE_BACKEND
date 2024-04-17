from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select 
from app.deps import get_db, get_current_user
from app.models import Booking, Waste , User , UserCreate , UserLogin
from typing import Annotated
from sqlalchemy.orm import registry
from fastapi.encoders import jsonable_encoder


mapper_registry = registry()


router=APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/booking" , status_code =201 )
async def booking(waste: Booking, db: Annotated[Session,  Depends(get_db)], current_user: Annotated[User, Depends(get_current_user)],  token: str = Depends(oauth2_scheme) ):
    

    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthenticated")
    
    
    # user =db.exec(select(User)).filter(User.email == current_user).first()
    waste = waste.model_dump()
    waste["user_id"] = current_user.id
    waste_create = Waste(**waste)
    db.add(waste_create)
    db.commit()
    db.refresh(waste_create)
    
    waste_create =jsonable_encoder(waste_create)
    
    return waste_create



    # waste_create.user = user
@router.on_event("startup")
async def startup_event():
    mapper_registry.configure()
    
  
  