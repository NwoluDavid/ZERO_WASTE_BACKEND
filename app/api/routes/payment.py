from fastapi import APIRouter

from app.utils import verify_payment
router = APIRouter()

@router.post("/verify-transaction{ref_id}")
async def verify_transaction(ref_id: str):
    "Verify the transaction id and provision the user"
    payment_status,data = verify_payment(ref_id)
    if payment_status == True:
        return data
    # get user in database by email
    # use that user id in getting bookings