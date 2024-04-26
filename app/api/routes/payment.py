from fastapi import APIRouter , Depends
from fastapi.responses import JSONResponse

from fastapi.encoders import jsonable_encoder
from app.utils import verify_payment

from app.models import Waste
from typing import Annotated

from sqlmodel import Session
from app.deps import get_db

router = APIRouter()

@router.post("/verify-transaction{ref_id}")
async def verify_transaction(ref_id: str,  db: Annotated[Session, Depends(get_db)]):
    "Verify the transaction id and provision the user"
    payment_status,data = verify_payment(ref_id)
    if payment_status == True:
    # booking = db.query(Waste).find(Waste.id == ref_id)
        booking = db.get(Waste, ref_id)
        booking.order_status = "COMPLETED"
    
    booking = jsonable_encoder(booking)
    
    return JSONResponse(
    status_code=201,
    content={
        "message": "payment successfully",
        "booking":booking
    })
        
 