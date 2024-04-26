from fastapi import APIRouter, Depends, HTTPException, status, Request  
from sqlmodel import Session

from app.deps import get_db, get_current_user
from app.models import UserCreate, User, UserUpdate

from typing import Annotated, Any
from app.utils import get_password_hash

from sqlalchemy.orm import registry
from sqlalchemy.exc import IntegrityError

from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from app.crud import get_user_by_email
from app.utils import create_token,send_email , generate_verification_email,verify_token





mapper_registry = registry()

router = APIRouter()

@router.post("/register" , response_model=UserCreate )
async def register(
    user: UserCreate, 
    db: Annotated[Session,  Depends(get_db)]
):
    """ this user registration route, take note  to put a valid phonenumber, start with the country code of the phonenumber.
    """
    db_email =db.query(User).filter(User.email ==user.email).first()
    
    if db_email is not None:
        raise  HTTPException(status_code = status.HTTP_400_BAD_REQUEST, 
            detail="User with the email already exists"
        )
    
    token = create_token(subject=user.email, type_ops="verify")
    data = generate_verification_email(email_to=user.email, email= user.email , token=token)
    send_email(email_to=user.email ,subject =data.subject, html_content = data.html_content)
        
    try:
        
        #hash the password 
        user.password = get_password_hash(user.password)
        new_user =User(**user.model_dump())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        new_user =jsonable_encoder(new_user)
        return JSONResponse(status_code =201, content={"data": new_user , "message": "user created successfully"})
    
    except Exception as e:
        error_message = "An error occurred while creating the user."   
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_message)
    
   
   


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




@router.get("/profile")
async def user_profile ( current_user: int = Depends(get_current_user), db: Session = Depends(get_db)):
    
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    user = current_user.model_dump()

    if not user:   
        raise HTTPException(status_code=404, detail="User not found")
    return jsonable_encoder(user)


   

@router.patch("/profile" , status_code=200)
async def update_user_profile(
    user_data: UserCreate, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """This route updates user profile.
    
    The user must be authenticated, else a 401 error will be returned, 
    indicating that the user is not authorized. If the user is not found,
    a 404 error will be returned.
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="User not authenticated")

    user = db.query(User).filter(User.email == current_user.email).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user_data.password =get_password_hash(user_data.password)
    # Update user profile fields
    for field, value in user_data.dict(exclude_unset=True).items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)

    user = jsonable_encoder(user)

    return JSONResponse(
        status_code=200,
        content={
            "message": "User profile updated successfully",
            "updated_profile": user
        }
    )



@router.delete("/profile", status_code=204 )
async def delete_user_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """this route deleted current user profile
    Current User can decide to delete his/her accout.

    If the user is not authenticated, returns a 401 Unauthorized error.
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    user = db.query(User).filter(User.email == current_user.email).first()
    
    db.delete(user)
    db.commit()
    db.refresh(user)
    
    user = jsonable_encoder(user)
    return JSONResponse(
        status_code=200,
        content={
            "message": "user deleted successfully",
            "deleted_user": user
        })






@router.on_event("startup")
async def startup_event():
    mapper_registry.configure()