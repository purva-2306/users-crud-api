
from getpass import getpass

from app.database.database import SessionLocal
from app.models import db_models
from app.core.security import hash_password


def create_teacher():
    db = SessionLocal()

    try:
        name = input("Enter teacher name: ").strip()
        email = input("Enter teacher email: ").strip().lower()
        phone = input("Enter teacher phone: ").strip()

        existing_user = db.query(db_models.User).filter(
            db_models.User.email == email
        ).first()

        if existing_user:
            print("This email is already registered.")
            print("No changes were made.")
            return

        password = getpass("Create teacher password: ")
        confirm_password = getpass("Confirm teacher password: ")

        if len(password) < 8:
            print("Password must contain at least 8 characters.")
            return

        if password != confirm_password:
            print("Passwords do not match.")
            return

        teacher = db_models.User(
            name=name,
            email=email,
            phone=phone,
            password_hash=hash_password(password),
            role="teacher",
            status="active"
        )

        db.add(teacher)
        db.commit()
        db.refresh(teacher)

        print("Teacher account created successfully!")
        print("Teacher ID:", teacher.id)
        print("Role:", teacher.role)

    except Exception:
        db.rollback()
        print("Teacher creation failed. Check your inputs and database connection.")

    finally:
        db.close()


if __name__ == "__main__":
    create_teacher()