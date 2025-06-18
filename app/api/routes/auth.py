from fastapi import APIRouter, status
from fastapi import APIRouter, Depends, HTTPException

from sqlmodel import Session
from typing import List

from app.deps import get_db
from app.models import NewPassword,Message

from app.models import ForgetPasswordRequest, ResetForgetPassword
from fastapi import BackgroundTasks

from app.utils import (
    send_email,
    verify_token,
    get_password_hash,
    create_token,
    generate_reset_password_email
)
from app.crud import get_user_by_email
from fastapi_mail import FastMail, MessageSchema, MessageType
from starlette.responses import JSONResponse

from starlette.background import BackgroundTasks
from typing import Annotated, Any

router=APIRouter()


@router.post("/verify-email/{token}")
async def verify_email(token: str, db: Annotated[Session, Depends(get_db)]):
    # verify token
    email = verify_token(token=token)

    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")

    user = get_user_by_email(session=db, email=email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this email does not exist in the system.",
        )

    user.is_active = True
    db.add(user)
    db.commit()
    db.refresh(user)
    return JSONResponse(status_code=201, content={"message": "Email verified"})

  
@router.post("/password-recovery/{email}")
async def recover_password(email: str, db: Annotated[Session, Depends(get_db)]):
    "Forgot password flow"
    user = get_user_by_email(session=db, email=email)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    password_reset_token = create_token(subject=email, type_ops="reset")

    # create email data
    email_data = generate_reset_password_email(
        email_to=user.email, email=email, token=password_reset_token
    )
    send_email(email_to=user.email ,subject =email_data.subject, html_content = email_data.html_content)
    return Message(message="Password recovery email sent")


@router.post("/reset-password/")
def reset_password(
    db: Annotated[Session, Depends(get_db)], body: NewPassword
) -> Message:
    """
    Reset password
    """
    email = verify_token(token=body.token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = get_user_by_email(session=db, email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this email does not exist in the system.",
        )
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="User is not Verified")
    
    hashed_password = get_password_hash(password=body.new_password)
    user.password = hashed_password
    
    for field, value in user.dict().items():
        setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    
    return Message(message="Password updated successfully")


    
        