from sqlmodel import Session, select
from app.models import User, UserUpdate, Review

from typing import List
from app.utils import verify_password

from starlette.background import BackgroundTasks
from pydantic import BaseModel

from fastapi_mail import FastMail, MessageSchema , MessageType
from jose import jwt , JWTError



def get_user_by_email(*, session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user

def authenticate(*, session: Session, email: str, password: str) -> User | None:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.password):
        return None
    return db_user




def get_user_by_id(db: Session, user_id: int) -> User:
    return db.get(User, user_id)

def update_user_patch(db: Session, user_id: int, user_data: UserUpdate) -> User:
    user = db.get(User, user_id)
    if not user:
        return None
    for field, value in user_data.dict(exclude_unset=True).items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user

def update_user(db: Session, user_id: int, user_data: UserUpdate) -> User:
    user = db.get(User, user_id)
    if not user:
        return None
    for field, value in user_data.dict().items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: int) -> User:
    user = db.get(User, user_id)
    if not user:
        return None
    db.delete(user)
    db.commit()
    return user

def create_review(db: Session, reviewer_name: str, rating: int, comment: str, user_id: int) -> Review:
    review = Review(reviewer_name=reviewer_name, rating=rating, comment=comment, user_id=user_id)
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


def update_review(db: Session, review_id: int, rating: int, comment: str) -> Review:
    review = db.get(Review, review_id)
    if not review:
        return None
    review.rating = rating
    review.comment = comment
    db.commit()
    db.refresh(review)
    return review

def get_reviews_by_user_id(db: Session, user_id: int) -> List[Review]:
    return db.query(Review).filter(Review.user_id == user_id).all()

def delete_review(db: Session, review_id: int) -> Review:
    review = db.get(Review, review_id)
    if not review:
        return None
    db.delete(review)
    db.commit()
    return review




