
from getpass import getpass

from app.database.database import SessionLocal
from app.models import db_models
from app.core.security import hash_password


db = SessionLocal()

try:
    email = input("Enter teacher email: ").strip().lower()

    teacher = db.query(db_models.User).filter(
        db_models.User.email == email,
        db_models.User.role == "teacher"
    ).first()

    if teacher is None:
        print("Teacher account not found.")
    else:
        password = getpass("Enter new password: ")
        confirm = getpass("Confirm new password: ")

        if len(password) < 8:
            print("Password must be at least 8 characters.")
        elif password != confirm:
            print("Passwords do not match.")
        else:
            teacher.password_hash = hash_password(password)
            db.commit()
            print("Teacher password updated successfully!")

except Exception:
    db.rollback()
    print("Password update failed.")

finally:
    db.close()