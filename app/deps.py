from sqlmodel import Session
from app.db import engine

from typing import Generator, Annotated
from app.config import settings

from fastapi import Depends, HTTPException
from app.utils import verify_token_access

from app.models import User
from fastapi.security import OAuth2PasswordBearer




reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/"
)


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]


def get_current_user(session: SessionDep, token: TokenDep) -> User:
    token_data = verify_token_access(token)


    user = session.get(User, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

