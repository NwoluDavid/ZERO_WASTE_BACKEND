from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel import Session, select
from app.deps import get_db, get_current_user
from app.models import UserCreate, User, UserUpdate
from typing import Annotated, Any
from app.utils import get_password_hash, save_profile_picture, validate_picture
from sqlalchemy.orm import registry
from sqlalchemy.exc import IntegrityError
from fastapi.responses import JSONResponse, FileResponse
from fastapi.encoders import jsonable_encoder
from fastapi import File, UploadFile
from botocore.client import Config
from fastapi import Response


from app.models import TokenData
from app.config import settings


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



@router.post("/user/profile-picture")
def upload_profile_picture(
    profile_picture: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    statement = select(User).where(User.id == current_user.id)
    db_user = db.exec(statement).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    changes_made = False
    if profile_picture:
        validate_picture(profile_picture)
        changes_made = True
        db_user.profile_picture = save_profile_picture(profile_picture)
        
    if changes_made:
        db.commit()
        return {"message": "User details updated successfully"}
    else:
        return {"message": "No changes made"}

@router.get("/user/profile-picture")
def get_profile_picture(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    statement = select(User.profile_picture).where(User.id == current_user.id)
    profile_picture = db.execute(statement).scalar()
    if not profile_picture:
        raise HTTPException(status_code=404, detail="Profile picture not found")
    return FileResponse(profile_picture)

