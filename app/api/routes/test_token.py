from fastapi import APIRouter, Depends
from app.deps import get_current_user

from app.models import User, UserOutput
from typing import Annotated, Any


router =APIRouter()


@router.post("/login/test-token", response_model=UserOutput)
def test_token(current_user: Annotated[User, Depends(get_current_user)]
) -> Any:
    """
    Test access token
    """
    return current_user