
import hashlib
import jwt

from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.models import db_models
from app.models.user import UserCreate
from app.core.security import hash_password, verify_password
from app.core.jwt import (
    create_access_token,
    create_refresh_token,
    decode_token
)


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


# REGISTER USER
def register_user(db: Session, user_data: UserCreate):
    existing_user = db.query(db_models.User).filter(
        db_models.User.email == user_data.email
    ).first()

    if existing_user:
        return None

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


# AUTHENTICATE USER
def authenticate_user(db: Session, email: str, password: str):
    user = db.query(db_models.User).filter(
        db_models.User.email == email
    ).first()

    if user is None or user.status != "active":
        return None

    if not verify_password(password, user.password_hash):
        return None

    return user


# CREATE LOGIN SESSION
def create_user_session(db: Session, user):
    refresh_token, expires_at = create_refresh_token(user.id)

    session = db_models.UserSession(
        user_id=user.id,
        refresh_token_hash=hash_token(refresh_token),
        expires_at=expires_at
    )

    db.add(session)
    db.flush()

    access_token = create_access_token(
        user.id,
        user.role,
        session.id
    )

    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


# REFRESH TOKENS
def refresh_user_session(db: Session, refresh_token: str):
    try:
        payload = decode_token(refresh_token)

        if payload.get("type") != "refresh":
            return None

        user_id = int(payload.get("sub"))

    except (jwt.InvalidTokenError, ValueError, TypeError):
        return None

    session = db.query(db_models.UserSession).filter(
        db_models.UserSession.refresh_token_hash == hash_token(refresh_token)
    ).first()

    if session is None:
        return None

    now = datetime.now(timezone.utc)

    if session.user_id != user_id:
        return None

    if session.revoked_at is not None:
        return None

    if session.expires_at <= now:
        return None

    user = db.query(db_models.User).filter(
        db_models.User.id == user_id
    ).first()

    if user is None or user.status != "active":
        return None

    # Revoke old session
    session.revoked_at = now

    # Create new refresh token and session
    new_refresh_token, new_expires_at = create_refresh_token(user.id)

    new_session = db_models.UserSession(
        user_id=user.id,
        refresh_token_hash=hash_token(new_refresh_token),
        expires_at=new_expires_at
    )

    db.add(new_session)
    db.flush()

    # Create access token linked to new session
    access_token = create_access_token(
        user.id,
        user.role,
        new_session.id
    )

    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }


# LOGOUT USER
def logout_user(db: Session, refresh_token: str):
    session = db.query(db_models.UserSession).filter(
        db_models.UserSession.refresh_token_hash == hash_token(refresh_token)
    ).first()

    if session is None or session.revoked_at is not None:
        return False

    session.revoked_at = datetime.now(timezone.utc)

    db.commit()

    return True