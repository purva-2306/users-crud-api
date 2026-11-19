
from sqlalchemy.orm import Session

from app.models import db_models
from app.models.user import UserCreate, UserUpdate
from app.core.security import hash_password


# CREATE USER
def create_user(db: Session, user_data: UserCreate):
    new_user = db_models.User(
        name=user_data.name,
        email=user_data.email,
        phone=user_data.phone,
        password_hash=hash_password(user_data.password),
        role="student",
        status=user_data.status
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# GET ALL USERS
def get_all_users(db: Session):
    return db.query(db_models.User).all()


# GET USER BY ID
def get_user_by_id(db: Session, user_id: int):
    return db.query(db_models.User).filter(
        db_models.User.id == user_id
    ).first()


# UPDATE USER
def update_user(db: Session, user_id: int, user_data: UserUpdate):
    user = get_user_by_id(db, user_id)

    if user is None:
        return None

    update_data = user_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)

    return user


# DELETE USER
def delete_user(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)

    if user is None:
        return False

    db.delete(user)
    db.commit()

    return True