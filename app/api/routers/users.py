
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database.database import get_db
from app.models.user import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserWithTasks
)
from app.models import db_models
from app.services import user_service
from app.core.dependencies import get_current_user, require_role

router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users"]
)


# CREATE USER - TEACHER ONLY
@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(require_role("teacher"))
):
    try:
        return user_service.create_user(db, user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists"
        )


# GET ALL USERS - TEACHER ONLY
@router.get("/", response_model=list[UserResponse])
def get_all_users(
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(require_role("teacher"))
):
    return user_service.get_all_users(db)


# GET USER DETAILS WITH TASKS
# TEACHER CAN VIEW ANY USER; STUDENT CAN VIEW OWN DATA
@router.get("/{user_id}/with-tasks", response_model=UserWithTasks)
def get_user_with_tasks(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(get_current_user)
):
    if current_user.role != "teacher" and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view your own data"
        )

    user = user_service.get_user_by_id(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


# GET USER BY ID
# TEACHER CAN VIEW ANY USER; STUDENT CAN VIEW OWN PROFILE
@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(get_current_user)
):
    if current_user.role != "teacher" and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view your own profile"
        )

    user = user_service.get_user_by_id(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


# UPDATE USER - TEACHER ONLY
@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(require_role("teacher"))
):
    updated_user = user_service.update_user(db, user_id, user)

    if updated_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return updated_user


# DELETE USER - TEACHER ONLY
@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(require_role("teacher"))
):
    deleted = user_service.delete_user(db, user_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return None