from fastapi import APIRouter, status
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
from app.config import settings
from app.crud import create_review, get_reviews_by_user_id, update_review, delete_review
from app.deps import get_db, get_current_user
from app.models import Review, User, ReviewBase
from app.models import ForgetPasswordRequest, ResetForgetPassword
from fastapi import BackgroundTasks
from app.utils import create_reset_password_token
from app.crud import get_user_by_email
from fastapi_mail import FastMail, MessageSchema, MessageType
from starlette.responses import JSONResponse
from starlette.background import BackgroundTasks

router=APIRouter()


@router.post("/password-recovery/{email}")
async def forget_password(email:str,
    db: Session = Depends(get_db)
    
):
    
    try: 
        user =get_user_by_email(session=db, email=email)
        # user =get_user_by_email()
        if user is None:
            raise HTTPException(status_code =status.HTTP_500_INTERNAL_SERVER_ERROR, detail ="Invalid Email address")

        
        
        secret_token = create_reset_password_token(email = user.email)
        # return secret_token
        forget_url_link = f"{settings.APP_HOST}{settings.FORGET_PASSWORD_URL}/{secret_token}"
        email_body = {"company_name": settings.MAIL_FROM_NAME,
                     "link_expiry_min": settings.FORGET_PASSWORD_LINK_EXPIRE_MINUTES,
                     "reset_link":forget_url_link}
        
        message = MessageSchema(
            subject= "Password Reset Instructions",
            recipients=[email],
            template_body=email_body,
            subtype=MessageType.html
        )
        
        template_name = "mail/password_reset.html"
        
        fm = FastMail(settings.conf)
        # background_tasks.add_task(fm.send_message, message, template_name)
        
        await fm.send_message(message)
        
        return JSONResponse(status_code=status.HTTP_200_OK,
        content={"message": "Email has been sent", "success": True,
        "status_code": status.HTTP_200_OK})
    except Exception as e:
        return e
  
        
# @router.post("/reset-password") 
# async def reset_password(
#     rfp: ResetForgetPassword,
#     db: Session = Depends(get_db)
# ):
#     try:
        
#         info =decode_reset_paaword_token(token =rfp.secret_token)
        
    
        