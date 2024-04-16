from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
from app.crud import create_review, get_reviews_by_user_id, update_review, delete_review
from app.deps import get_db
from app.models import Review

router = APIRouter()


@router.post("/reviews/", response_model=Review , status_code =201)
def create_review_route(reviewer_name: str, rating: int, comment: str, user_id: int, db: Session = Depends(get_db)):
    review = create_review(db, reviewer_name, rating, comment, user_id)
    return review

@router.put("/reviews/{review_id}/", response_model=Review,status_code =201)
def update_review_route(review_id: int, rating: int, comment: str, db: Session = Depends(get_db)):
    review = update_review(db, review_id, rating, comment)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

@router.get("/reviews/user/{user_id}/", response_model=List[Review] ,status_code =200)
def get_reviews_by_user_id_route(user_id: int, db: Session = Depends(get_db)):
    reviews = get_reviews_by_user_id(db, user_id)
    return reviews

@router.delete("/reviews/{review_id}/", response_model=Review , status_code =200)
def delete_review_route(review_id: int, db: Session = Depends(get_db)):
    review = delete_review(db, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

