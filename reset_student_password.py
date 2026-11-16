
from getpass import getpass

from app.database.database import SessionLocal
from app.models import db_models
from app.core.security import hash_password


db = SessionLocal()

try:
    email = input("Enter student email: ").strip()

    user = db.query(db_models.User).filter(
        db_models.User.email == email,
        db_models.User.role == "student"
    ).first()

    if user is None:
        print("Student not found!")
    else:
        password = getpass("Enter new student password: ")
        confirm = getpass("Confirm new password: ")

        if password != confirm:
            print("Passwords do not match!")
        elif len(password) < 8:
            print("Password must be at least 8 characters!")
        else:
            user.password_hash = hash_password(password)
            db.commit()
            print("Student password updated successfully!")

finally:
    db.close()