from fastapi import APIRouter
from .routes import items, login, users, test_token, reviews ,booking, auth ,Admin,payment


api_router = APIRouter()

api_router.include_router(auth.router , prefix="/forgotpassword", tags=["Auth"])
api_router.include_router(users.router, prefix="/users", tags=["User"])
api_router.include_router(login.router, tags=["User"])
api_router.include_router(Admin.router, prefix="/admin", tags=["Admin"])
api_router.include_router(booking.router, prefix="/bookings", tags=["Booking"])
api_router.include_router(reviews.router, prefix="/reviews", tags=["Reviews"])
api_router.include_router(items.router, prefix="/items", tags=["Items"])
api_router.include_router(test_token.router, prefix="/utils", tags=["Utils"])
api_router.include_router(payment.router, prefix="/payment", tags=["payment"])