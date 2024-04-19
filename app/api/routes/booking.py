from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session
from app.deps import get_db, get_current_user
from app.models import Booking, Waste, User
from typing import List
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/booking", status_code=201)
async def booking(
    waste: Booking,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    token: str = Depends(oauth2_scheme)
):
    """ This is the booking route. It first checks if a user is authorized before the user can place a booking.
        If the user is not authorized, a 401 error will be raised.
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    waste = waste.model_dump()
    waste["user_id"] = current_user.id
    Waste.user = current_user.id
    waste_create = Waste(**waste)
    db.add(waste_create)
    db.commit()
    db.refresh(waste_create)
    
    return waste_create

@router.get("/bookings", response_model=List[Booking], status_code=200)
async def get_bookings_by_user(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """ This route gets a user's booking orders from the database.
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    user_bookings = db.query(Waste).filter(Waste.user_id == current_user.id).all()

    return user_bookings

@router.on_event("startup")
async def startup_event():
    pass
