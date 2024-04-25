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




mapper_registry = registry()

router = APIRouter()

@router.post("/register" )
async def register(
    user: UserCreate, 
    db: Annotated[Session,  Depends(get_db)]
):
    """ this user registration route, take note  to put a valid phonenumber, start with the country code of the phonenumber.
    """
    db_email =db.query(User).filter(User.email ==user.email).first()
    
    if db_email is not None:
        return  HTTPException(status_code = status.HTTP_400_BAD_REQUEST, 
            detail="User with the email already exists"
        )
    
    db_username =db.query(User).filter(User.first_name == user.first_name and User.last_name == user.last_name).first()
      
    if db_username is not None:
        return  HTTPException(status_code = status.HTTP_400_BAD_REQUEST, 
            detail="User with the email already exists"
        )
     
        
    try:
        
        user
        
        #hash the password 
        user.password = get_password_hash(user.password)
        
        new_user =User(**user.model_dump())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        
    except IntegrityError as e:
        error_message ="Email already exists"
        raise HTTPException(status_code=409, detail=error_message)
    except Exception as e:
    
        error_message = "An error occurred while creating the user."    
        raise HTTPException(status_code=500, detail=error_message)
    # return { status_code= "message": "User created successfully"}
    new_user =jsonable_encoder(new_user)
    return JSONResponse(status_code =201, content={"data": new_user , "message": "user created successfully"})



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


@router.on_event("startup")
async def startup_event():
    mapper_registry.configure()


@router.get("/profile")
def user_profile ( current_user: int = Depends(get_current_user), db: Session = Depends(get_db)):
    
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    user = current_user.model_dump()

    if not user:   
        raise HTTPException(status_code=404, detail="User not found")
    return jsonable_encoder(user)

@router.post("/verify-email/{token}")
async def verify_email(token:str , db : Annotated[Session, Depends(get_db)]):
    
    email = verify_token(token = token)
    
    if not email:
        raise HTTPException(status_code =400, detail ="Invalid token")
    
    user =await get_user_by_email(email = email)
    
    if not user:
        raise HTTPException(
            status_code =500,
            detail ="The user with this email does not exist in the system"
        )
    
    # Making the user to be active.
    
    user.is_active = True
    return JSONResponse(status_code =201, content={"message": "Email verified" , "user":user})
   

@router.patch("/profile")
def user_profile(
    user_data: UserUpdate, 
    current_user: int = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):
    
    if not current_user:
        raise HTTPException(status_code=404, detail="User not authenticated")
    
    user_data = User(**user_data.model_dump())
    db.add(user_data)
    db.commit()
    db.refresh(user_data)
    return user_data

@router.put("/profile")
def user_profile(user_data: UserUpdate, current_user: int = Depends(get_current_user), db: Session = Depends(get_db)):
    if not  current_user:
        raise HTTPException(status_code=404, detail="User not authenticated")
    user_data = User(**user_data.model_dump())
    db.add(user_data)
    db.commit()
    db.refresh(user_data)
    return user_data
@router.delete("/profile")
def user_profile(user_data: UserUpdate, current_user: int = Depends(get_current_user), db: Session = Depends(get_db)):
    if not  current_user:
        raise HTTPException(status_code=404, detail="User not authenticated")
    # user_data = User(**user_data.model_dump())

    # deleted_user = delete_user(db, current_user.user_id)
    # if not deleted_user:
    #     raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}


