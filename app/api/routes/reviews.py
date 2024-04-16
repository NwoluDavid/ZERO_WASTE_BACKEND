from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
from app.crud import create_review, get_reviews_by_user_id, update_review, delete_review
from app.deps import get_db, get_current_user
from app.models import Review, User, ReviewBase

router = APIRouter()


@router.post("/reviews/", response_model=Review , status_code =201)
def review_route(reviewer_name: str, rating: int, comment: str, db: Session = Depends(get_db) ):
    review = create_review(db, reviewer_name, rating, comment)
    return review

# Update a review by ID
@router.put("/reviews/{review_id}/", response_model=Review, status_code=200)
def review_route(review_id: int, review_data: ReviewBase, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Check if the current user is authenticated
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthenticated")
    
    # Update the review
    review = update_review(db, review_id, review_data, current_user.id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review


# Read reviews by user ID
@router.get("/reviews/", response_model=List[Review], status_code=200)
def reviews_by_user_route(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Check if the current user is authenticated
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthenticated")
    
    # Get reviews for the current user
    reviews = get_reviews_by_user_id(db, current_user.id)
    return reviews



# Delete a review by ID
@router.delete("/reviews/{review_id}/", status_code=204 , status_code =200)
def review_route(review_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Check if the current user is authenticated
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthenticated")
    
    # Delete the review
    success = delete_review(db, review_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Review not found")

