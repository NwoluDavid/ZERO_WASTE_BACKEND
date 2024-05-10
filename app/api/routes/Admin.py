from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlmodel import Session, select


from app.deps import get_current_user , get_db
from app.models import User, UserCreate, UserUpdate

from sqlalchemy.orm import registry
from fastapi.encoders import jsonable_encoder

from app.utils import get_password_hash
from sqlalchemy.exc import IntegrityError

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


mapper_registry = registry()

router = APIRouter()


@router.get("/")
async def hello():
    return {"message": "Hello World"}


@router.get(
    "/users/",
    response_model=List[User],
    summary="Get a list of users.",
    response_description="List of users retrieved successfully.",
)
async def read_users(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
):
    """
    Retrieve a list of users.

    Args:
        current_user (User, optional): The current authenticated user.
        session (Session, optional): The database session.
        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Maximum number of records to return. Defaults to 10.

    Returns:
        List[User]: List of users retrieved successfully.
    """
    if not current_user.is_staff:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only staff members can access this route.",
        )
    users = session.exec(select(User).offset(skip).limit(limit)).all()
    users= jsonable_encoder(users)
    return JSONResponse(
    status_code=200,
    content={
        "message": "list of users",
        "users":users
    })
    


@router.post(
    "/users/",
    response_model=User,
    status_code =201,
    summary="Create a new user.",
    response_description="User created successfully.",
)
async def create_user(
    user: UserCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Create a new user.

    Args:
        user_create (UserCreate): Details of the user to be created.
        current_user (User, optional): The current authenticated user.
        session (Session, optional): The database session.

    Returns:
        User: User created successfully.
    """
    if not current_user.is_staff:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only staff members can access this route.",
        )
    
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
        
        
    # except IntegrityError as e:
    #     error_message ="Email already exists"
    #     raise HTTPException(status_code=409, detail=error_message)
    except Exception as e:
        error_message = "An error occurred while creating the user."    
        raise HTTPException(status_code=500, detail=error_message)
    # return { status_code= "message": "User created successfully"}
    new_user =jsonable_encoder(new_user)
    return JSONResponse(status_code =201, content={"data": new_user , "message": "user created successfully"})


@router.get(
    "/users/{user_id }",
    status_code=200,
    response_model=User,
    summary="Get user by ID.",
    response_description="User retrieved successfully.",
)
async def read_user_by_id(
    user_id: str= Path(..., title="The UUID of the user."),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Retrieve a user by ID.

    Args:
        user_id (UUID): The UUID of the user to retrieve.
        current_user (User, optional): The current authenticated user.
        session (Session, optional): The database session.

    Returns:
        User: User retrieved successfully.
    """
    if not current_user.is_staff:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only staff members can access this route.",
        )
    
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
            )
    return user


@router.put(
    "/users/{user_id}",
    response_model=User,
    summary="Update user by ID.",
    response_description="User updated successfully.",
)
async def update_user(
    user_update:UserUpdate,
    user_id: str = Path(..., title="The UUID of the user."),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Update a user by ID.

    Args:
        user_id (UUID): The UUID of the user to update.
        user_update (UserUpdate): Details of the user to update.
        current_user (User, optional): The current authenticated user.
        session (Session, optional): The database session.

    Returns:
        User: User updated successfully.
    """
    if not current_user.is_staff:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only staff members can access this route.",
        )
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )
    for field, value in user_update.dict().items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user


@router.delete(
    "/users/{user_id}",
    summary="Delete user by ID.",
    response_description="User deleted successfully.",
)
async def delete_user(
    user_id: str = Path(..., title="The UUID of the user."),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Delete a user by ID.

    Args:
        user_id (UUID): The UUID of the user to delete.
        current_user (User, optional): The current authenticated user.
        session (Session, optional): The database session.

    Returns:
        dict: Message indicating user deletion.
    """
    if not current_user.is_staff:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only staff members can access this route.",
        )
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully."}



@router.on_event("startup")
async def startup_event():
    mapper_registry.configure()