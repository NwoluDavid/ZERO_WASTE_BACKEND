from fastapi import APIRouter, Depends, HTTPException, Query , Path
from fastapi.responses import JSONResponse

from sqlmodel import Session
from typing import List

from app.crud import create_review, get_reviews_by_user_id, update_review, delete_review
from app.deps import get_db, get_current_user

from app.models import Review, User, ReviewBase
from typing import Annotated

from fastapi.encoders import jsonable_encoder

router = APIRouter()




@router.post("/review", status_code=201)
async def create_review(
    comment:Annotated[str | None, Query(max_length=300)],
    reviewer_name:Annotated[str | None , Query(max_length=50)] = None,
    rating: Annotated[str | None, Query()] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new review.

    Args:
        comment (str): The comment or review text.
        reviewer_name (str): The name of the reviewer.
        rating (int): The rating given by the reviewer.
        db (Session, optional): The database session. Defaults to Depends(get_db).
        current_user (User, optional): The current authenticated user. Defaults to Depends(get_current_user).

    Returns:
        Review: The newly created review.

    Raises:
        HTTPException: If the user is not authenticated.

    Response status code:
        - 201 Created: If the review was successfully created.
        - 401 Unauthorized: If the user is not authenticated.

    Response JSON:
        - data (Review): The newly created review.
        - message (str): A message indicating the review was created successfully.
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthenticated")

    review = Review(
        comment=comment,
        reviewer_name=reviewer_name,
        rating=rating,
        user_id=current_user.id
    )
    
    # review["user_id"] = current_user.id
    
    db.add(review)
    db.commit()
    db.refresh(review)
    
    review  = jsonable_encoder(review )
    
    return JSONResponse(
        status_code=200,
        content={
            "message": "review created successfully",
            "created_review": review 
        })
    
 
    
# Read reviews made by the current user
@router.get("/review/", response_model=List[Review], status_code=200)
def reviews_by_user_route(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)):
    # Check if the current user is authenticated
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthenticated")
    


    user_review = db.query(Review).filter(Review.user_id == current_user.id).all()

    return user_review



# Update a review by ID , made by the current user.
@router.put("/review/{review_id}/", response_model=Review, status_code=200)
def review_route( 
    comment:Annotated[str | None, Query(max_length=300)],
    reviewer_name:Annotated[str | None , Query(max_length=50)] = None,
    rating: Annotated[str | None, Query()] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    review_id: int = Annotated[int |None, Path()],
    
    
    ):
    """ This route update review made by the current user
    
    """
    
    # Check if the current user is authenticated
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthenticated")
    
    review = db.get(Review, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    if review.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized to delete this review")
    
    
    # Update the review
    update_review = Review(
        reviewer_name=reviewer_name,
        rating=rating,
        comment=comment,
        id=review_id,
        user_id=current_user.id
    )
      
    
    for field, value in update_review.dict().items():
        setattr(review, field, value)
    
    db.commit()
    db.refresh(review)

    review  = jsonable_encoder(review )

    return JSONResponse(
        status_code=200,
        content={
            "message": "review updated successfully",
            "updated_review": review 
        })
    
    
  



# Delete a review by ID
@router.delete("/review/{review_id}/", status_code=204 )
def review_route(review_id: int = Annotated[int |None, Path()], current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Check if the current user is authenticated
    
    # Delete the review
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    review = db.get(Review, review_id)
    if not review :
        raise HTTPException(status_code=404, detail="Booking not found")
    
    if review .user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized to delete this booking")
    
    db.delete(review )
    db.commit()
    
    review  = jsonable_encoder(review )
    
    return JSONResponse(
        status_code=200,
        content={
            "message": "review deleted successfully",
            "deleted_review": review 
        })

