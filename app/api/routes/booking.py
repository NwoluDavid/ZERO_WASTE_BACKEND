from fastapi import APIRouter, Depends, HTTPException,Path
from fastapi.security import OAuth2PasswordBearer

from sqlmodel import Session
from app.deps import get_db, get_current_user

from app.models import Booking, Waste, User,UpdateDeliveryStatus
from typing import List

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from typing import Annotated

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/booking", status_code=201, response_model =Waste)
async def booking(
    waste: Booking,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """ This is the booking route. It first checks if a user is authorized before the user can place a booking.
        If the user is not authorized, a 401 error will be raised.
        
        In the type of waste we only have , Plastic, Medical , Organic and Industrial , 
        ensure to write exactly the way I have written here, in other to get the right status code.
        
        
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    user =current_user
    
    waste = waste.model_dump()
    waste["user_id"] = current_user.id
    waste_create = Waste(**waste)
    waste_create.user = user
    
    db.add(waste_create)
    db.commit()
    db.refresh(waste_create)
    
    waste_create = jsonable_encoder(waste_create)
    
    return JSONResponse(
    status_code=201,
    content={
        "message": "booking created successfully",
        "booking":waste_create
    })
    

@router.get("/booking", response_model=List[Waste], status_code=200)
async def get_bookings_by_user(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """ This route gets a user's booking orders from the database.
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    user_bookings = db.query(Waste).filter(Waste.user_id == current_user.id).all()
    
 
    user_bookings = jsonable_encoder(user_bookings)
    return  user_bookings
   


@router.delete("/booking/{booking_id}", status_code=204 )
async def delete_booking(
    booking_id: Annotated[str,Path(discription="Add the booking ID , which is uuid" , examples="eaec7763-0996-4d39-bca6-547335d9cb18")],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a booking by its ID.

    If the user is not authenticated, returns a 401 Unauthorized error.
    If the booking does not exist, returns a 404 Not Found error.
    if the booking dooes not belong to the current user return 403 unauthorized to delete this booking
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    booking = db.get(Waste, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    if booking.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized to delete this booking")
    
    db.delete(booking)
    db.commit()
    
    booking = jsonable_encoder(booking)
    return JSONResponse(
        status_code=200,
        content={
            "message": "Booking deleted successfully",
            "deleted_booking": booking
        })

    



@router.patch("/booking/{booking_id}", response_model=UpdateDeliveryStatus, status_code = 200)
async def update_booking(
    booking_id: Annotated[str ,Path(discription="Add the booking ID , which is uuid" , examples="eaec7763-0996-4d39-bca6-547335d9cb18")],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update a booking delivery status by its ID.

    If the user is not authenticated, returns a 401 Unauthorized error.
    If the booking does not exist, returns a 404 Not Found error.
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    booking = db.get(Waste, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    if booking.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized to delete this booking")
    
    booking.delivery_status = True
    
    # Update the booking with the new data
    for field, value in booking.dict().items():
        setattr(booking, field, value)
    
    db.commit()
    db.refresh(booking)
    
    booking = jsonable_encoder(booking)
    
    booking
    return JSONResponse(
    status_code=200,
    content={
        "message": "booking delivery status updated successfully",
        "booking":booking
    })
    

@router.put("/booking/{booking_id}", response_model=Waste , status_code =200)
async def replace_booking(
    booking_id: Annotated[str, Path(discription ="Add the booking id, note id is an int", example="eaec7763-0996-4d39-bca6-547335d9cb18")],
    updated_booking: Booking,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Replace a booking by its ID.

    If the user is not authenticated, returns a 401 Unauthorized error.
    If the booking does not exist, returns a 404 Not Found error.
    if the booking does not belong to the user, return 403 Unauthorized to delete this booking
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    booking = db.get(Waste, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    if booking.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized to delete this booking")
    
    
    # Delete the existing booking and create a new one with the updated data
    for field, value in updated_booking.dict().items():
        setattr(booking, field, value)
    
    db.commit()
    db.refresh(booking)
    
    booking = jsonable_encoder(booking)
    
    return JSONResponse(
    status_code=200,
    content={
        "message": "bookimg updated successfully",
        "created_review": booking
    })


@router.on_event("startup")
async def startup_event():
    pass


